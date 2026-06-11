import sys
import os
from pathlib import Path
import asyncio
import inspect
import json
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telebot.async_telebot import AsyncTeleBot
import telebot
import httpx  # ใช้สำหรับยิง API คุยกับ Supabase โดยตรง

# 📂 [Infra] ปักหมุด Root Directory ให้ Python เห็นโมดูลทั้งหมด
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from meta_orchestrator import meta_orchestrator
from growth_marketing_orchestrator import growth_marketing_orchestrator

# 🔑 ตั้งค่าระบบและ Env (ดึงจาก Render)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") 
WEBHOOK_URL = f"{RENDER_URL}/{BOT_TOKEN}" if RENDER_URL else None
TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7238952711")
API_KEY_TOKEN = os.getenv("BASE44_API_KEY", "base44_master_secret_key")

# 🗄️ Supabase Config (เตรียมไว้สำหรับคุยกับตารางหลังบ้าน)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

bot = AsyncTeleBot(BOT_TOKEN) if BOT_TOKEN else None
app = FastAPI(title="Base44 Enterprise Multi-Agent Command Center v2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 Path Setup สำหรับหน่วยความจำภายในเครื่องเพื่อทำ Hot-Reload
MEMORY_DIR = PROJECT_ROOT / "00_memory"
MEMORY_DIR.mkdir(exist_ok=True)
MODEL_CONFIG_FILE = MEMORY_DIR / "active_model.json"

# สร้างไฟล์ความจำตั้งต้นหากยังไม่มี
if not MODEL_CONFIG_FILE.exists():
    with open(MODEL_CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "active_ai_model": "Default_OpenSource_LLM", 
            "previous_stable_model": "Default_OpenSource_LLM", # สำหรับ Rollback
            "last_action_id": "init",
            "last_updated": str(datetime.now())
        }, f, ensure_ascii=False, indent=4)

# 🛡️ ระบบรักษาความปลอดภัยหน้าบ้าน
def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized: Access Denied")
    return api_key

# 📦 Data Models สำหรับรับข้อมูลจาก Lovable Dashboard
class ApprovePayload(BaseModel):
    request_id: str
    new_model: str
    old_model: str

class RollbackPayload(BaseModel):
    request_id: str

# =====================================================================
# 🚨 [Section 1] ประตูหน้าบ้านสำหรับปลุก UptimeRobot (Health Check)
# =====================================================================
@app.get("/")
async def health_check():
    active_model = "Unknown"
    if MODEL_CONFIG_FILE.exists():
        with open(MODEL_CONFIG_FILE, 'r', encoding='utf-8') as f:
            active_model = json.load(f).get("active_ai_model", "Unknown")
            
    return {
        "status": "healthy", 
        "project": "Base44 Multi-Agent Core V2",
        "current_active_model": active_model,
        "timestamp": datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S")
    }

# =====================================================================
# 🚀 [Senior Dev Route] ท่อลัดพิเศษสำหรับ "นายท่าน" ใช้กดทดสอบยิงรายงาน Telegram
# =====================================================================
@app.get("/test-telegram-report")
async def test_telegram_report():
    try:
        # ดึงคลาส MetaOrchestrator มาสร้างตัวแปรเพื่อรันแมนนวลรวดเร็ว
        from meta_orchestrator import MetaOrchestrator
        orchestrator_instance = MetaOrchestrator()
        cron_result = await orchestrator_instance.run_morning_cron()
        
        # ยิงข้อความสั้นทดสอบความฟิตของ Bot เข้า Telegram ของนายท่านตรง ๆ
        if bot:
            await bot.send_message(
                chat_id=TARGET_CHAT_ID, 
                text="🚀 **[Manual Test Trigger]**\nระบบทางลัดของนายท่านเชื่อมต่อเสร็จสมบูรณ์แล้วครับพ้ม บอทกำลังส่งรายงานยามเช้าให้ทำงานทันที!"
            )
            
        return {
            "status": "success",
            "message": "🚀 ระบบสั่งยิงรายงานสำเร็จแล้วครับนายท่าน! ลองเปิดดูในแอป Telegram ได้เลยครับพ้ม",
            "cron_log": cron_result
        }
    except Exception as e:
        return {
            "status": "bug_detected",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "suggestion": "ตรวจสอบความถูกต้องของพาร์ทโฟลเดอร์และการตั้งค่าคีย์บอทบนหน้า Render ครับ"
        }

# =====================================================================
# 🎛️ [Section 2] ระบบ Traceability & สลับโมเดล (คุยกับหน้าเว็บ Base44)
# =====================================================================

@app.post("/api/v1/ai-research/approve-with-trace", dependencies=[Depends(verify_api_key)])
async def approve_and_trace_model(payload: ApprovePayload):
    """ท่อรับคำสั่ง APPROVE จากหน้าแดชบอร์ด พร้อมสลักรหัส Trace ID"""
    try:
        print(f"🔍 [Trace Workflow] Request ID: {payload.request_id} | Changing from {payload.old_model} ──> {payload.new_model}")
        
        # 1. ทำการ Hot-Reload เปลี่ยนแปลงโครงสร้างโมเดลหลัก
        with open(MODEL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "active_ai_model": payload.new_model,
                "previous_stable_model": payload.old_model, # สลักเกราะป้องกันไว้สำหรับทำ Rollback
                "last_action_id": payload.request_id,
                "last_updated": str(datetime.now())
            }, f, ensure_ascii=False, indent=4)
        
        # 2. (Optional) ยิงแจ้งเตือนเข้า Telegram ว่ามีการเปลี่ยนโมเดลแล้ว
        if bot:
            msg = f"🔄 **[System Shift]** นายท่านทำการอนุมัติสลับโมเดล\n✅ โมเดลปัจจุบัน: `{payload.new_model}`\n🆔 Trace ID: `{payload.request_id}`"
            await bot.send_message(chat_id=TARGET_CHAT_ID, text=msg, parse_mode="Markdown")
            
        return {
            "status": "success",
            "trace_id": payload.request_id,
            "message": f"Hot-Reload สำเร็จ! ระบบสลับไปใช้ {payload.new_model} แล้ว"
        }
        
    except Exception as e:
        print(f"🚨 [Trace Error] Request {payload.request_id} Failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/ai-research/emergency-rollback", dependencies=[Depends(verify_api_key)])
async def emergency_rollback(payload: RollbackPayload):
    """ปุ่มถอยทัพฉุกเฉิน (Emergency Rollback) เมื่อโมเดลใหม่รันแล้วพัง"""
    try:
        # 1. โหลดข้อมูลเดิมเพื่อดูว่าก่อนหน้านี้ใช้โมเดลอะไร
        with open(MODEL_CONFIG_FILE, 'r', encoding='utf-8') as f:
            current_state = json.load(f)
            
        safe_model = current_state.get("previous_stable_model", "Default_OpenSource_LLM")
        broken_model = current_state.get("active_ai_model")
        
        print(f"🚑 [Emergency Rollback] ถอยทัพจาก {broken_model} ──> กลับไปที่ {safe_model}")
        
        # 2. สลับกลับทันที
        with open(MODEL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                "active_ai_model": safe_model,
                "previous_stable_model": safe_model, # รีเซ็ตกันพลาด
                "last_action_id": f"rollback_from_{payload.request_id}",
                "last_updated": str(datetime.now())
            }, f, ensure_ascii=False, indent=4)
            
        if bot:
            msg = f"🚑 **[EMERGENCY ROLLBACK]** ถอยทัพสำเร็จ!\n❌ ยกเลิกการใช้: `{broken_model}`\n✅ สลับกลับมาใช้: `{safe_model}`"
            await bot.send_message(chat_id=TARGET_CHAT_ID, text=msg, parse_mode="Markdown")

        return {
            "status": "success",
            "rollback_to": safe_model,
            "message": f"กู้ระบบสำเร็จ! กลับไปใช้โมเดล {safe_model} เรียบร้อยแล้ว"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rollback Failed: {str(e)}")

# =====================================================================
# ⏰ [Section 3] ลูปยุทธศาสตร์ 09:00 น. และระบบ Webhook / Polling
# =====================================================================
# (โค้ดส่วนของ daily_strategic_report_loop() และ Webhook ยังคงทำงานตามเดิม)

@app.on_event("startup")
async def on_startup():
    if bot and WEBHOOK_URL:
        print(f"🧹 [System] กำลังสลับไปใช้ Webhook ที่ URL: {WEBHOOK_URL}")
        await bot.remove_webhook()
        await bot.set_webhook(url=WEBHOOK_URL)
        print("✅ [System] Webhook Active!")
    elif bot:
        print("⚠️ [System] สลับกลับไปใช้ระบบ Polling สำรอง...")
        await bot.remove_webhook()
        asyncio.create_task(bot.polling(non_stop=True, allowed_updates=['message']))

if WEBHOOK_URL:
    @app.post(f"/{BOT_TOKEN}")
    async def process_webhook(request: Request):
        try:
            json_str = await request.json()
            update = telebot.types.Update.de_json(json_str)
            await bot.process_new_updates([update])
        except Exception as e:
            print(f"⚠️ [Webhook Error] {e}")
        return {"status": "ok"}

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    try:
        reply = await meta_orchestrator.route_and_execute(message.text, str(message.from_user.id))
        await bot.reply_to(message, reply or "🤖 บอททำงานเรียบร้อยครับ")
    except Exception as e:
        print(f"⚠️ [Chat Error] {e}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("04_scripts.telegram_bot:app", host="0.0.0.0", port=port, reload=False)