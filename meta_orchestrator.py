import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# [Meta-Orchestrator: รับคำสั่งและจ่ายงาน]
class MetaOrchestrator:
    async def process(self, text):
        msg = text.lower()
        if "analyze" in msg:
            # รายงาน BU.1 ส่วนที่ 1
            await self.send_telegram("🔍 ดร.แสงสุข กำลังสแกนตลาด... \n\n1. สินค้า A\n2. สินค้า B\n3. สินค้า C\n\n(พิมพ์ชื่อสินค้าเพื่อเลือกทำ Content)")
        elif len(msg) > 3:
            # รายงาน BU.1 ส่วนที่ 2 (Content)
            await self.send_telegram(f"🚀 กำลังเขียนคอนเทนต์ให้: {msg}...")
            
    async def send_telegram(self, text):
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_BOT_TOKEN')}/sendMessage",
                json={"chat_id": os.environ.get("TELEGRAM_CHAT_ID"), "text": text}
            )

# [Routes: ต้องมีครบเพื่อให้ Render และ UptimeRobot ไม่ฟ้อง]
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return {"status": "ok"}

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health(): return Response(status_code=200)

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    asyncio.create_task(MetaOrchestrator().process(data.get("message", {}).get("text", "")))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))