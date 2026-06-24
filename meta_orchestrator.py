import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# เลือกโมเดลที่ใช้งานได้จริงโดยอัตโนมัติ เพื่อป้องกัน error 404 Not Found
try:
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(models[0].name)
    print(f"Log: ระบบเลือกใช้โมเดล {models[0].name}")
except:
    model = genai.GenerativeModel('gemini-1.5-flash')

class MetaOrchestrator:
    async def log_to_sheets(self, product, content):
        sheet_url = os.environ.get("APPS_SCRIPT_URL")
        if not sheet_url: return
        payload = {"product": product, "hook": "AI Generated", "solution": content}
        async with httpx.AsyncClient() as client:
            try: await client.post(sheet_url, json=payload, timeout=10.0)
            except: pass

    async def process(self, text):
        msg = text.strip()
        if "analyze" in msg.lower():
            await self.send_telegram("🔍 ดร.แสงสุข กำลังสแกนตลาด...\n\n1. สินค้า A\n2. สินค้า B\n3. สินค้า C\n\n(พิมพ์ชื่อสินค้าเพื่อเลือกทำ Content)")
        elif len(msg) > 2 and "analyze" not in msg.lower():
            await self.send_telegram(f"🚀 กำลังเขียนคอนเทนต์ให้: {msg}...")
            try:
                response = model.generate_content(f"เขียนคอนเทนต์ปิดการขายสั้นๆ สำหรับ: {msg}")
                content = response.text
                await self.send_telegram(f"🚀 [สำเร็จ]:\n\n{content}")
                await self.log_to_sheets(msg, content)
            except Exception as e:
                await self.send_telegram(f"❌ ระบบมีปัญหาครับ: {e}")

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

# แก้ปัญหา 404 ที่ Root และ Health
@app.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
@app.api_route("/health", methods=["GET", "HEAD", "OPTIONS"])
async def root(): return Response(status_code=200, content="OK")

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))