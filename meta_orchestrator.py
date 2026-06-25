import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()

# --- ระบบจัดการ Multi-Provider & Failover ---
class AIProvider:
    @staticmethod
    async def call(prompt):
        # ลำดับการเรียกใช้: Google Gemini -> Groq -> OpenRouter -> DeepSeek
        providers = [
            {"name": "Gemini", "func": AIProvider.call_gemini},
            {"name": "Groq", "func": AIProvider.call_groq},
            {"name": "OpenRouter", "func": AIProvider.call_openrouter},
            {"name": "DeepSeek", "func": AIProvider.call_deepseek}
        ]
        
        for p in providers:
            try:
                return await p["func"](prompt)
            except Exception as e:
                print(f"Provider {p['name']} failed: {e}")
        return "ขออภัย ระบบไม่สามารถประมวลผลได้ในขณะนี้"

    @staticmethod
    async def call_gemini(prompt):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # ใช้ gemini-1.5-flash ตามชื่อที่ถูกต้องในระบบ
        model = genai.GenerativeModel('gemini-1.5-flash')
        return (await asyncio.to_thread(model.generate_content, prompt)).text

    @staticmethod
    async def call_groq(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions", 
                headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"},
                json={"model": "llama3-70b-8192", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

    @staticmethod
    async def call_openrouter(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
                json={"model": "meta-llama/llama-3-70b-instruct", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

    @staticmethod
    async def call_deepseek(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('DEEPSEEK_API_KEY')}"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

# --- BU.1 & CEO Logic ---
class BU1_Orchestrator:
    async def run_bu1_pipeline(self, query):
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        payload = {"q": f"best selling affiliate products for {query}", "num": 5}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            raw = [item.get("title") for item in resp.json().get("organic", [])]
        
        prompt = f"จากข้อมูล: {raw} คัดเลือกสินค้า Affiliate 3 รายการ และของฟรี 1 รายการ. ตอบรูปแบบ: สินค้า1: ... สินค้า2: ... สินค้า3: ... ของฟรี: ..."
        return await AIProvider.call(prompt)

class MetaOrchestrator:
    def __init__(self):
        self.bu1 = BU1_Orchestrator()

    async def process(self, text):
        msg = text.strip()
        if "analyze" in msg.lower():
            await self.send_telegram("🏢 [CEO คุณศุภจี]: เริ่มวิเคราะห์ตลาดผ่านเครือข่าย Multi-Provider...")
            res = await self.bu1.run_bu1_pipeline(msg.replace("analyze", "").strip())
            await self.send_telegram(f"✅ [รายงาน BU.1]:\n{res}")
        else:
            await self.send_telegram(f"✍️ [คุณอนิศ]: กำลังปั้นคอนเทนต์สำหรับ {msg}...")
            content = await AIProvider.call(f"เขียนคอนเทนต์ Affiliate ขาย {msg} ให้ปิดการขายได้ทันที")
            await self.send_telegram(f"🚀 [คอนเทนต์]:\n{content}")

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}