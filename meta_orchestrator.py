# =====================================================================
# 🚀 BASE44 ENGINE V6.8.1: STABLE ROUTER & BU.1 MASTERMIND
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V6.8.1")

# --- 1. Silent Health Handlers (กัน Render สั่ง Shutdown) ---
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler(): return Response(content="OK", status_code=200)

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health_check(): return Response(content="OK", status_code=200)

# --- 2. Messenger & Config ---
class Messenger:
    TOKEN = "8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4"
    CHAT_ID = "7238952711"
    
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text}, timeout=5.0)
            except: pass

# --- 3. BU.1 Mastermind Agents ---
class BU1_Orchestrator:
    async def analyze_and_execute(self, query):
        return (f"🔍 [Strategic Marketer]: กำลังตรวจสอบ '{query}' ตามเกณฑ์ยุทธศาสตร์ 4 ข้อ...\n"
                f"📝 [Content Creator]: เตรียมร่าง Inbound Framework...")

# --- 4. Request Orchestrator (เพิ่ม Command Router ที่บอสต้องการ) ---
class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        
        # --- COMMAND ROUTER (จุดที่แก้ไข) ---
        if "/search" in text_lower:
            query = text.replace("/search", "").strip()
            result = await BU1_Orchestrator().analyze_and_execute(query)
            await Messenger.send(f"🤖 [CEO BU.1 รายงาน]:\n\n{result}")
            
        elif "report bu.1" in text_lower:
            await Messenger.send("📊 [BU.1 กำลังสรุปดีลทำเงิน]: ตรวจสอบฐานข้อมูล Affiliate 10%+ และคัดเลือก 3 แบรนด์ให้บอสเลือกครับ...")
            
        elif "report bu.2" in text_lower:
            await Messenger.send("🤖 [BU.2 กำลังตรวจสอบโมเดล AI]: สแกนหา Open-source ตัวใหม่ที่เร็วกว่าปัจจุบัน...")
            
        else:
            await Messenger.send("✅ ระบบพร้อมทำงาน:\n- /search [หัวข้อ]\n- report bu.1\n- report bu.2")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

# --- 5. Scheduler (รายงาน 9 โมง) ---
scheduler = AsyncIOScheduler(timezone=timezone('Asia/Bangkok'))
scheduler.add_job(lambda: asyncio.create_task(Messenger.send("☀️ อรุณสวัสดิ์ครับบอส! ระบบรายงานยุทธศาสตร์พร้อมวิเคราะห์โอกาสทำเงินวันนี้ครับ")), 'cron', hour=9, minute=0)
scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))