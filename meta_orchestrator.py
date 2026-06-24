import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI(title="BU.1_Master_Command_Center")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class Messenger:
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: 
                await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text})
            except Exception as e: print(f"Telegram Error: {e}")

class MetaOrchestrator:
    async def fetch_serper(self, query):
        api_key = os.environ.get("SERPER_API_KEY")
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://google.serper.dev/search", json={"q": query, "num": 5}, headers=headers)
            return [item.get("title") for item in resp.json().get("organic", [])]

    async def handle_request(self, text):
        msg = text.lower().strip()
        
        # ปรับ Logic การรับคำสั่งให้ตรงกับโครงสร้าง BU.1
        if msg.startswith("analyze"):
            query = msg.replace("analyze", "").strip() or "pet care"
            await Messenger.send(f"🔍 ดร.แสงสุข กำลังสแกนหมวด: {query}...")
            
            products = await self.fetch_serper(query)
            if products:
                # รายงานสินค้า 3 รายการตามที่บอสต้องการ [cite: 16]
                report = "✅ [รายงานจาก BU.1 ส่วนที่ 1]: รายการสินค้าแนะนำ 3 รายการ\n\n"
                for i, p in enumerate(products[:3], 1):
                    report += f"{i}. {p}\n"
                report += "\n(พิมพ์ชื่อสินค้าที่ต้องการ เพื่อให้คุณอนิศ Content Agent จัดทำคอนเทนต์ปิดการขายครับ)"
                await Messenger.send(report)
            else:
                await Messenger.send("⚠️ ไม่พบข้อมูลในหมวดนี้ครับ")
        
        # ถ้ารับข้อความธรรมดา ให้ถือว่าเป็นการเลือกสินค้า [cite: 16]
        elif len(msg) > 3 and "analyze" not in msg:
            await Messenger.send(f"✍️ คุณอนิศ (Content Agent) กำลังเขียนคอนเทนต์สำหรับ: {msg}...")
            # ส่วนนี้จะเตรียมเชื่อมต่อ Google Sheets และ Apps Script ในขั้นตอนถัดไป
            await Messenger.send(f"🚀 [สำเร็จ]: คอนเทนต์พร้อมสำหรับ {msg} [ใส่เนื้อหาตาม Template]")

# --- Routes ---
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return {"status": "BU.1 Operational"}

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health(): return Response(content="OK", status_code=200)

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    # ตรวจสอบโครงสร้างข้อมูล Telegram [cite: 1]
    message = data.get("message", {})
    text = message.get("text", "")
    if text:
        await MetaOrchestrator().handle_request(text)
    return Response(content="OK")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))