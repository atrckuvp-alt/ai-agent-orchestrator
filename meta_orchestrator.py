import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# แทนที่บรรทัด model = ... ด้วยชุดนี้ครับ
try:
    # สั่งให้ AI หาโมเดลที่พร้อมใช้งานที่สุดจาก Account ของบอส
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if models:
        model = genai.GenerativeModel(models[0].name)
    else:
        model = genai.GenerativeModel('gemini-1.5-flash') # fallback
except Exception as e:
    model = genai.GenerativeModel('gemini-1.5-flash')

class MetaOrchestrator:
    async def log_to_sheets(self, product, content):
        sheet_url = os.environ.get("APPS_SCRIPT_URL")
        if not sheet_url: return
        payload = {"product": product, "hook": "AI Generated", "solution": content}
        async with httpx.AsyncClient() as client:
            await client.post(sheet_url, json=payload, timeout=10.0)

    async def process(self, text):
        msg = text.strip()
        if "analyze" in msg.lower():
            query = msg.lower().replace("analyze", "").strip() or "ทั่วไป"
            await self.send_telegram(f"🔍 ดร.แสงสุข กำลังสแกนหมวด: {query}...")
            products = ["CAT PILLOW", "PET COLLAR", "SMART FEEDER"]
            await self.send_telegram(f"✅ รายการสินค้า:\n1. {products[0]}\n2. {products[1]}\n3. {products[2]}\n\n(พิมพ์ชื่อสินค้าเพื่อรับคอนเทนต์)")

        elif len(msg) > 2 and "analyze" not in msg.lower():
            await self.send_telegram(f"✍️ คุณอนิศกำลังเขียนคอนเทนต์สำหรับ: {msg}...")
            # บอทจะใช้โมเดล gemini-1.0-pro ที่ตั้งไว้ด้านบน
            response = model.generate_content(f"เขียนคอนเทนต์ปิดการขายสำหรับ: {msg}")
            content = response.text
            await self.send_telegram(f"🚀 [สำเร็จ]:\n\n{content}")
            await self.log_to_sheets(msg, content)

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

# [ข้อ ข: เพิ่ม Route /health เพื่อให้ Uptime Monitor ไม่ฟ้อง 404]
@app.api_route("/health", methods=["GET", "HEAD"])
async def health(): return Response(status_code=200)

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return {"status": "Enterprise Ready"}

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))