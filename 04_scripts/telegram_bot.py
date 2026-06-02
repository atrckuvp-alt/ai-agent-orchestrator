import os
import json
from pathlib import Path
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update

# โหลดค่าคอนฟิกูเรชันพื้นฐาน
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# URL ของแอปคุณบน Render (เช่น https://your-app.onrender.com)
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") 

if not TOKEN:
    raise ValueError("❌ ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables")

# สตาร์ทบอทและตัวดักจับข้อความ (Aiogram 3.x Pattern)
bot = Bot(token=TOKEN)
dp = Dispatcher()
# สตาร์ทตัวแอปเว็บเซิร์ฟเวอร์ FastAPI เพื่อคุยกับ Render
app = FastAPI()

# สัญญาลักษณ์ตำแหน่งโฟลเดอร์สำหรับตรวจสอบสิทธิ์
ALLOWED_USERS = [7238952711]

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# --- [ระบบรับข้อความผ่าน WEBHOOK] ---
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Endpoint สำหรับรับข้อมูลที่ Telegram ยิงตรงเข้ามาระหว่างทำงาน"""
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        print(f"⚠️ [Webhook Feed Error]: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def health_check():
    """ระบบตรวจจับสถานะบอท (Health Check) ป้องกัน Render ตบแอปตาย"""
    return {"status": "healthy", "bot_name": "AI Command Center", "mode": "webhook"}

# --- [ระบบ LIFESPAN / STARTUP HOOKS] ---
@app.on_event("startup")
async def on_startup():
    """ฟังก์ชันสั่งการทำงานอัตโนมัติเมื่อเว็บเซิร์ฟเวอร์สตาร์ทอัพ"""
    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/webhook"
        print(f"🔗 [Webhook Setup] Setting webhook to: {webhook_url}")
        # สั่งล้าง Polling เก่าออกป้องกันอาการชนกัน และผูกท่อ Webhook ทันที
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=webhook_url)
    else:
        print("⚠️ [Webhook Warning] ไม่พบ RENDER_EXTERNAL_URL ระบบจะไม่ผูกท่อกับ Telegram อัตโนมัติ")

# --- [TELEGRAM HANDLERS ZONE] ---
@dp.message(types.Message, lambda message: message.text in ["/start", "/menu"])
async def show_menu_command(message: types.Message):
    """ดักจับคำสั่งระบบพื้นฐาน"""
    await message.answer("🤖 *ยินดีต้อนรับสู่ AI Command Center!* ตอนนี้ระบบย้ายมาอยู่บนฐานระบบ Webhook เสถียร 100% แล้วครับ สามารถสั่งงานด้วยภาษาธรรมชาติได้ทันที")

@dp.message()
async def handle_text_message(message: types.Message):
    """ดักจับข้อความภาษาธรรมชาติ ยิงตรงเข้าโมดูลเอเจนท์ Dynamic"""
    user_id = message.from_user.id
    text = message.text

    if not is_allowed(user_id):
        await message.answer("🔒 ขออภัยครับ บัญชีของคุณไม่ได้ลงทะเบียนเข้าใช้งานระบบ")
        return

    print(f"📥 [Webhook Bot] Received Natural Language from {user_id}: '{text}'")

    status_msg = await message.answer(
        "🧠 *รับทราบคำสั่งครับ...* [Webhook Mode] กำลังส่งต่อให้ Meta Orchestrator จัดสรรทีมงานปฏิบัติการสักครู่ครับ"
    )

    try:
        from workflow_builder import execute_user_objective
        result = await execute_user_objective(objective=text, user_id=user_id)

        if result.get("success"):
            await status_msg.edit_text(result.get("message"), parse_mode="Markdown")
        else:
            await status_msg.edit_text(f"⚠️ เกิดข้อขัดข้องระหว่างประมวลผล:\n{result.get('message')}")

    except Exception as e:
        print(f"❌ [Bot Pipeline Crash]: {e}")
        await status_msg.edit_text(f"❌ ไม่สามารถส่งต่อคำสั่งเข้าสู่ระบบสมองส่วนกลางได้\nError: {str(e)[:200]}")