import os
import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") 

if not TOKEN:
    raise ValueError("❌ ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables")

# 1. ประกาศตัวแปรบอทและตัวดักจับข้อความรอไว้
bot = Bot(token=TOKEN)
dp = Dispatcher()

ALLOWED_USERS = [7238952711]

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# 2. 🎯 [⚡ ไม้ตายด่านสำคัญ] ระบบ Lifespan จัดการวงจรชีวิตบอทและผูกท่อ Webhook อัตโนมัติ
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ฟังก์ชันควบคุมการเปิด-ปิดระบบบอทให้ปลอดภัยและซ่อมพอร์ตถาวร"""
    if RENDER_URL:
        webhook_url = f"{RENDER_URL}/"
        print(f"🚀 [Lifespan Startup] ล้างท่อ Polling เก่า และผูก Webhook ไปที่: {webhook_url}")
        # สั่งล้างอัปเดตเก่าที่ค้างในระบบ Telegram ป้องกันอาการชนกัน
        await bot.delete_webhook(drop_pending_updates=True)
        # ผูกท่อ Webhook เข้าพาร์ทหลักตรงๆ ตามที่ Render เรียกใช้
        await bot.set_webhook(url=webhook_url)
    else:
        print("⚠️ [Lifespan Warning] ไม่พบ RENDER_EXTERNAL_URL ระบบจะไม่เซ็ต Webhook ให้")
        
    yield  # ⏸️ ให้เซิร์ฟเวอร์ FastAPI รันทำงานรับช่วงต่อตามปกติ
    
    # 🛑 ทำงานตอนเซิร์ฟเวอร์โดนสั่งปิด (Graceful Shutdown)
    print("🔌 [Lifespan Shutdown] กำลังปิดการเชื่อมต่อเซสชันบอท...")
    await bot.session.close()

# 3. สร้างแอป FastAPI โดยผูกระบบควบคุมวงจรชีวิต (lifespan) เข้าไปด้วย
app = FastAPI(lifespan=lifespan)

# --- [🔗 ระบบรับข้อมูล WEBHOOK] ---
@app.post("/")
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """รับข้อมูลดิบในรูปแบบ JSON แปลงส่งเข้า Aiogram สยบบั๊ก BaseModel 100%"""
    try:
        # ดึงค่า Dict ดิบๆ ส่งตรงให้ Dispatcher ชำแหละโครงสร้างเองภายในเฟรมเวิร์ก
        json_data = await request.json()
        await dp.feed_update(bot=bot, update=json_data)
        return {"status": "ok"}
    except Exception as e:
        print(f"⚠️ [Webhook Feed Error]: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def health_check():
    """ระบบตอบกลับสัญญาณตรวจสุขภาพของ Render"""
    return {"status": "healthy", "bot_name": "AI Command Center", "mode": "webhook"}

# --- [TELEGRAM HANDLERS ZONE] ---
@dp.message(types.Message, lambda message: message.text in ["/start", "/menu"])
async def show_menu_command(message: types.Message):
    await message.answer("🤖 *ยินดีต้อนรับสู่ AI Command Center!* ระบบ Webhook ผ่านท่อ Lifespan ทำงานสมบูรณ์ 100% แล้วครับ!")

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