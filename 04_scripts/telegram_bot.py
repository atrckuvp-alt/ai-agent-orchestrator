import os
import json
from pathlib import Path
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") 

if not TOKEN:
    raise ValueError("❌ ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables")

bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()

ALLOWED_USERS = [7238952711]

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# --- [🔗 📍 แก้ไขจุดนี้: ควบรวมพาร์ทหน้าแรกให้รองรับ POST จาก Telegram ได้ทันที] ---
@app.post("/")
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """รองรับทั้งยิงเข้าพาร์ทหลัก / และพาร์ท /webhook เพื่อดักจับ 405 Method Not Allowed"""
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
    """คงไว้สำหรับการตรวจเช็คสุขภาพของระบบ Render (GET)"""
    return {"status": "healthy", "bot_name": "AI Command Center", "mode": "webhook"}

# --- [ระบบ STARTUP HOOKS] ---
@app.on_event("startup")
async def on_startup():
    if RENDER_URL:
        # บังคับผูกท่อเข้าที่พาร์ทหลักเพื่อความชัวร์และตรงกับล็อกที่ Telegram ส่งมา
        webhook_url = f"{RENDER_URL}/"
        print(f"🔗 [Webhook Setup] Setting webhook target to: {webhook_url}")
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=webhook_url)
    else:
        print("⚠️ [Webhook Warning] ไม่พบ RENDER_EXTERNAL_URL")

# --- [TELEGRAM HANDLERS ZONE] ---
@dp.message(types.Message, lambda message: message.text in ["/start", "/menu"])
async def show_menu_command(message: types.Message):
    await message.answer("🤖 *ยินดีต้อนรับสู่ AI Command Center!* ระบบ Webhook ซ่อมแซมท่อส่งสัญญาณเสร็จสิ้น 100% แล้วครับ")

@dp.message()
async def handle_text_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if not is_allowed(user_id):
        await message.answer("🔒 ขอภัยครับ บัญชีของคุณไม่ได้ลงทะเบียนเข้าใช้งานระบบ")
        return

    print(f"📥 [Webhook Working!] Processing Natural Language: '{text}'")

    status_msg = await message.answer(
        "🧠 *รับทราบคำสั่งครับ...* กำลังวิเคราะห์และส่งงานต่อให้โมดูลหลังบ้านประมวลผลสักครู่ครับ"
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
        await status_msg.edit_text(f"❌ ไม่สามารถส่งต่อคำสั่งได้\nError: {str(e)[:200]}")