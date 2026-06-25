import os, asyncio, uvicorn, httpx
import google.generativeai as genai
from fastapi import FastAPI, Request, Response

app = FastAPI()

# --- 1. Health Check (ทำให้ Log สะอาด ไม่มี 404/405) ---
@app.api_route("/", methods=["GET", "HEAD", "POST"])
@app.api_route("/health", methods=["GET", "HEAD", "POST"])
async def health_check():
    return Response(status_code=200, content="OK")

# --- 2. ระบบ Multi-Provider (สลับใช้ค่ายอื่นอัตโนมัติหาก Gemini พัง) ---
class AIProvider:
    @staticmethod
    async def call(prompt):
        providers = [
            {"name": "Gemini", "func": AIProvider.call_gemini},
            {"name": "Groq", "func": AIProvider.call_groq},
            {"name": "OpenRouter", "func": AIProvider.call_openrouter}
        ]
        for p in providers:
            try:
                return await p["func"](prompt)
            except Exception as e:
                print(f"Provider {p['name']} failed, switching... Error: {str(e)[:50]}")
        return "ระบบประมวลผลติดปัญหา กรุณาลองใหม่อีกครั้ง"

    @staticmethod
    async def call_gemini(prompt):
        # ใช้โมเดล gemini-2.0-flash หรือรุ่นที่บอสใช้งานได้
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash') 
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text

    @staticmethod
    async def call_groq(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

    @staticmethod
    async def call_openrouter(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
                json={"model": "meta-llama/llama-3.1-70b-instruct", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

# --- 3. Orchestrator Core (พร้อมระบบพ่น Error เข้า Telegram) ---
class MetaOrchestrator:
    async def process(self, text):
        try:
            msg = text.strip()
            if "analyze" in msg.lower():
                await self.send_telegram("🏢 [CEO คุณศุภจี]: เริ่มวิเคราะห์ตลาดผ่านเครือข่าย Multi-Provider...")
                res = await AIProvider.call(f"วิเคราะห์และคัดเลือกสินค้า Affiliate จาก: {msg}")
                await self.send_telegram(f"✅ [รายงาน BU.1]:\n{res}")
            else:
                await self.send_telegram(f"✍️ [คุณอนิศ]: กำลังปั้นคอนเทนต์ขาย {msg}...")
                content = await AIProvider.call(f"เขียนคอนเทนต์ Affiliate ขาย {msg} ให้ปิดการขายได้ทันที")
                await self.send_telegram(f"🚀 [คอนเทนต์]:\n{content}")
        except Exception as e:
            error_text = f"❌ [SYSTEM CRASHED]: {str(e)}"
            print(error_text)
            await self.send_telegram(error_text)

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