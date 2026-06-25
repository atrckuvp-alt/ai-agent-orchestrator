import os, asyncio, uvicorn, httpx
import google.generativeai as genai
from fastapi import FastAPI, Request, Response

app = FastAPI()

# 1. Health Check Endpoint (แก้ปัญหา 404/405 ใน Log ของ Render)
@app.api_route("/", methods=["GET", "HEAD", "POST"])
@app.api_route("/health", methods=["GET", "HEAD", "POST"])
async def health_check():
    return Response(status_code=200, content="OK")

# 2. ระบบ Multi-Provider (The Failover Engine)
class AIProvider:
    @staticmethod
    async def call(prompt):
        # ลำดับการเรียกใช้: Google -> Groq -> OpenRouter -> DeepSeek
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
                print(f"Provider {p['name']} failed, trying next... Error: {str(e)[:50]}")
        return "ระบบประมวลผลติดปัญหา กรุณาลองใหม่อีกครั้ง"

    @staticmethod
    async def call_gemini(prompt):
        # ใช้โมเดลที่ตั้งค่าไว้ใน Env หรือ default เป็น 2.5-flash ตามหน้า Usage ของบอส
        model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel(model_name)
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text

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

# 3. Core Logic (Orchestrator)
class MetaOrchestrator:
    async def process(self, text):
        msg = text.strip()
        try:
            if "analyze" in msg.lower():
                await self.send_telegram("🏢 [CEO คุณศุภจี]: เริ่มวิเคราะห์ตลาดผ่านเครือข่าย Multi-Provider...")
                # เรียกใช้ Pipeline (สมมติว่ามี BU1_Orchestrator อยู่แล้ว)
                res = await AIProvider.call(f"วิเคราะห์และคัดเลือกสินค้า Affiliate จาก: {msg}")
                await self.send_telegram(f"✅ [รายงาน BU.1]:\n{res}")
            else:
                await self.send_telegram(f"✍️ [คุณอนิศ]: กำลังปั้นคอนเทนต์ขาย {msg}...")
                content = await AIProvider.call(f"เขียนคอนเทนต์ Affiliate ขาย {msg} ให้ปิดการขายได้ทันที")
                await self.send_telegram(f"🚀 [คอนเทนต์]:\n{content}")
        except Exception as e:
            await self.send_telegram(f"❌ [System Error]: {str(e)}")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))