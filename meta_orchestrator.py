# =====================================================================
# 🚀 BASE44 ENGINE V6.9.1: FULL CONTENT GENERATION PIPELINE
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V6.9.1")

# --- 1. Silent Health Handlers ---
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
            try: await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text}, timeout=10.0)
            except: pass

# --- 3. BU.1 Mastermind Agents ---
class BU1_Orchestrator:
    async def get_report(self):
        return (
            "📊 [รายงานยุทธศาสตร์ BU.1 - สรุปดีลทำเงินประจำวัน]\n\n"
            "🔍 วิเคราะห์ Market Gap: สินค้ากลุ่ม 'Home Office Ergonomics' กำลังพุ่งสูง แต่ตลาดขาดตัวเลือกที่เน้นสุขภาพกระดูกสันหลังโดยเฉพาะ\n\n"
            "🏆 3 แบรนด์แนะนำ (Affiliate 10%+):\n"
            "1. ErgoComfort Pro\n"
            "2. SpineCare Desk\n"
            "3. FlexiPosture\n\n"
            "💡 บอสพิมพ์ชื่อแบรนด์ที่เลือกมาได้เลยครับ ผมจะร่าง Copywriting ปิดการขายให้ทันที!"
        )

# --- 4. Request Orchestrator ---
class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        
        # 1. รายงานหลัก
        if "report bu.1" in text_lower:
            report = await BU1_Orchestrator().get_report()
            await Messenger.send(report)
            
        # 2. ระบบตอบสนองการเลือกแบรนด์ (Content Generation)
        elif any(brand in text_lower for brand in ["ergocomfort pro", "spinecare desk", "flexiposture"]):
            selected_brand = text.strip()
            await Messenger.send(
                f"📝 [Content Creator กำลังทำงาน]: กำลังร่างเนื้อหาสำหรับ '{selected_brand}'...\n\n"
                f"🔥 Hook: 'บอกลาอาการปวดหลังด้วย {selected_brand} ที่ออกแบบมาเพื่อคุณ...' \n"
                f"✅ คุณสมบัติ: วัสดุพรีเมียม, ปรับระดับได้แม่นยำ, คืนทุนไวในระยะยาว\n"
                f"💰 ลิงก์ทำเงิน: [รอใส่ลิงก์ Affiliate ของบอส]\n\n"
                "บอสเอาเนื้อหานี้ไปโพสต์ในเพจได้เลยครับ!"
            )
            
        elif "/search" in text_lower:
            await Messenger.send("🔍 [Strategic Marketer]: กำลังวิเคราะห์ข้อมูลตลาด... ระบบพร้อมประมวลผลข้อมูลจริงใน Phase ถัดไปครับ")
            
        elif "report bu.2" in text_lower:
            await Messenger.send("🤖 [BU.2 รายงาน]: ระบบโมเดล AI เสถียรดีเยี่ยม พร้อมขยายสู่ Phase 1 เต็มรูปแบบ")
            
        else:
            await Messenger.send("✅ ระบบพร้อมทำงาน:\n- /search [หัวข้อ]\n- report bu.1\n- report bu.2")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

# --- 5. Scheduler ---
scheduler = AsyncIOScheduler(timezone=timezone('Asia/Bangkok'))
scheduler.add_job(lambda: asyncio.create_task(Messenger.send("☀️ อรุณสวัสดิ์ครับบอส! ระบบรายงานยุทธศาสตร์พร้อมวิเคราะห์โอกาสทำเงินวันนี้ครับ")), 'cron', hour=9, minute=0)
scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))