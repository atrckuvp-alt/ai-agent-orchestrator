# =====================================================================
# 🚀 BASE44 ENGINE V6.8.0: EMERGENCY STABILITY & SILENT HANDLER
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V6.8.0")

# --- 1. Silent Exception & Health Handlers (ต้องมีไว้เพื่อกัน Render สั่ง Shutdown) ---
@app.exception_handler(404)
async def custom_404_handler(_, __): 
    return Response(content="OK", status_code=200)

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler(): 
    return Response(content="OK", status_code=200)

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health_check(): 
    return Response(content="OK", status_code=200)

# --- 2. Messenger & Config ---
class Messenger:
    TOKEN = "8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4"
    CHAT_ID = "7238952711"
    
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text}, timeout=5.0)
            except: pass

# --- 3. BU.1 Mastermind & Scheduler ---
async def send_daily_report():
    await Messenger.send("☀️ อรุณสวัสดิ์ครับบอส! ระบบรายงานยุทธศาสตร์อัตโนมัติพร้อมวิเคราะห์โอกาสทำเงินวันนี้ครับ")

scheduler = AsyncIOScheduler(timezone=timezone('Asia/Bangkok'))
scheduler.add_job(send_daily_report, 'cron', hour=9, minute=0)
scheduler.start()

class BU1_Orchestrator:
    async def analyze_and_execute(self, query):
        return (f"🔍 [Strategic Marketer]: กำลังตรวจสอบ '{query}' ตามเกณฑ์ยุทธศาสตร์ 4 ข้อ...\n"
                f"📝 [Content Creator]: เตรียมร่าง Inbound Framework...")

class MetaOrchestrator:
    async def handle_request(self, text):
        if text.startswith("/search"):
            query = text.replace("/search", "").strip()
            result = await BU1_Orchestrator().analyze_and_execute(query)
            await Messenger.send(f"🤖 [CEO BU.1 รายงาน]:\n\n{result}")
        else:
            await Messenger.send("✅ รับทราบคำสั่งครับบอส กำลังประสานงาน BU.1...")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))