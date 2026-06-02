import os
import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.filters import Command

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") 

if not TOKEN:
    raise ValueError("❌ ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables")

# 1. ประกาศตัวแปรบอทและตัวดักจับข้อความ
bot = Bot(token=TOKEN)
dp = Dispatcher()

ALLOWED_USERS = [7238952711]

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# 2. ระบบ Lifespan สำหรับจัดการ Webhook อย่างปลอดภัยสูงสุด
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ควบคุมวงจรการเชื่อมต่อ Webhook เพื่อไม่ให้เกิดปัญหาสายชนกัน"""
    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/"
        print(f"🚀 [Lifespan Startup] ล้างท่อ Polling เก่า และผูก Webhook ไปที่: {webhook_url}")
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(url=webhook_url)
    else:
        print("⚠️ [Lifespan Warning] ไม่พบ RENDER_EXTERNAL_URL")
        
    yield  # ปล่อยให้ระบบเว็บรันทำงานต่อตามปกติ
    
    print("🔌 [Lifespan Shutdown] กำลังปิดเซสชันบอทอย่างปลอดภัย...")
    await bot.session.close()

# 3. สร้างแอป FastAPI พร้อมเชื่อมต่อ Lifespan
app = FastAPI(lifespan=lifespan)

# --- [🔗 ระบบรับข้อมูล WEBHOOK] ---
@app.post("/")
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """ดักจับและคัดกรองข้อมูลจาก Telegram แปลงเข้าสู่ระบบแบบเสถียร 100%"""
    try:
        json_data = await request.json()
        
        # 🛡️ ระบบ Bulletproof Parsing: ป้องกันข้อผิดพลาดของ Pydantic ทุกสถานการณ์
        update = None
        try:
            # กลยุทธ์ที่ 1: แปลงแบบมาตรฐาน Pydantic v2 (ไม่ใส่ context ป้องกันบั๊ก positional argument)
            update = Update.model_validate(json_data)
        except Exception as e1:
            try:
                # กลยุทธ์ที่ 2: แปลงแบบส่ง bot context เข้าไปด้วย
                update = Update.model_validate(json_data, context={"bot": bot})
            except Exception as e2:
                try:
                    # กลยุทธ์ที่ 3: รองรับระบบ Pydantic v1 (สำหรับสภาพแวดล้อมเก่า)
                    update = Update.parse_obj(json_data)
                except Exception as e3:
                    raise ValueError(f"ไม่สามารถแปลงโครงสร้าง JSON เป็น Update Object ได้: {e3}")
        
        # ยิงวัตถุ Update ตัวจริงเข้าสู่ระบบ Dispatcher 
        await dp.feed_update(bot=bot, update=update)
        return {"status": "ok"}
    except Exception as e:
        print(f"⚠️ [Webhook Feed Error]: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def health_check():
    """ตอบกลับสำหรับระบบตรวจเช็คสุขภาพของ Render (Health Check)"""
    return {"status": "healthy", "bot_name": "AI Command Center", "mode": "webhook"}

# --- [TELEGRAM HANDLERS ZONE] ---
@dp.message(Command("start", "menu"))
async def show_menu_command(message: types.Message):
    await message.answer("🤖 *ยินดีต้อนรับสู่ AI Command Center!* ระบบเชื่อมต่อผ่านสัญญาณตรง Webhook สำเร็จแล้วครับ พร้อมคุยภาษาธรรมชาติได้ทันที")

@dp.message()
async def handle_text_message(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    if not is_allowed(user_id):
        await message.answer("🔒 ขออภัยครับ บัญชีของคุณไม่ได้ลงทะเบียนเข้าใช้งานระบบ")
        return

    print(f"📥 [Webhook Working!] Processing Natural Language from {user_id}: '{text}'")

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
