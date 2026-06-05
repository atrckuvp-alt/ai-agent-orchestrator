# Complete file: 04_scripts/telegram_bot.py (With Strict Thailand Time Zone & ASGI App Fix)
import os
import sys
import asyncio
import datetime
from pathlib import Path
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

load_dotenv(dotenv_path=ROOT / ".env")
from meta_orchestrator import meta_orchestrator

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("💥 ไม่พบ TELEGRAM_BOT_TOKEN ในระบบ Environment Variables!")

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

# 🌐 🔥 [ASGI APP FIX FOR RENDER] 🔥
# สร้างตัวแปรหลอกไว้ให้ Uvicorn ตรวจสอบผ่าน ไม่ปิดเซิฟเวอร์หนี
async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({
            'type': 'http.response.body',
            'body': b'AI Orchestrator Command Center Is Operating Smoothly.',
        })

# =====================================================================
# ⏰ [PLAN A - CHRONOS WATCHER TIME-ZONE FIXED] 
# =====================================================================
async def autonomous_cron_loop(bot_instance, target_user_id: int):
    print("⏳ [Chronos Watcher] ระบบเฝ้าระวังเวลาเปิดทำงานคู่ขนาน...")
    has_run_today = False
    
    while True:
        try:
            tz_thailand = datetime.timezone(datetime.timedelta(hours=7))
            now = datetime.datetime.now(tz_thailand)
            
            if now.hour == 9 and now.minute == 0:
                if not has_run_today:
                    print("🔔 [Chronos Trigger] ได้เวลา 09:00 น. ตรงในไทย สั่งเดินเครื่องรายงาน!")
                    await bot_instance.send_message(
                        chat_id=target_user_id, 
                        text="⏰ **[Morning Briefing]** อรุณสวัสดิ์ครับนายท่าน! ระบบเริ่มประมวลผลรายงานยุทธศาสตร์ประจำวันอัตโนมัติแล้วครับ..."
                    )
                    scheduled_result = await meta_orchestrator.execute_scheduled_task(user_id=target_user_id)
                    
                    if scheduled_result and "data" in scheduled_result and "message" in scheduled_result["data"]:
                        await bot_instance.send_message(chat_id=target_user_id, text=scheduled_result["data"]["message"])
                    has_run_today = True
            else:
                if now.hour != 9 or now.minute != 0:
                    has_run_today = False
                    
            await asyncio.sleep(20)
        except Exception as cron_err:
            print(f"⚠️ [Chronos Warning] ลูปเวลาติดขัด: {cron_err}")
            await asyncio.sleep(30)

# =====================================================================
# 💬 [TELEGRAM MESSAGES GATEWAY LOGIC]
# =====================================================================
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    welcome_text = (
        "🤖 **AI Command Center (v2.2)**\n\n"
        "🟢 ระบบความปลอดภัย 5 ชั้น (Active)\n"
        "🟢 บังคับฐานเวลาประเทศไทย 09:00 น. (Fixed)\n"
        "🟢 ยูนิต Growth Marketing BU (Ready)"
    )
    await bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    user_id = message.from_user.id
    user_text = message.text
    
    print(f"📥 [Incoming Message] จาก {user_id}: {user_text}")
    orchestrator_response = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
    
    if orchestrator_response and "data" in orchestrator_response:
        data_payload = orchestrator_response["data"]
        if "message" in data_payload:
            await bot.send_message(chat_id=message.chat.id, text=data_payload["message"])

if __name__ == "__main__":
    async def main():
        MY_USER_ID = 7238952711
        asyncio.create_task(autonomous_cron_loop(bot_instance=bot, target_user_id=MY_USER_ID))
        print("📡 [Polling Active] บอทออนไลน์รอคำสั่งนายท่าน 24 ชั่วโมง...")
        await bot.infinity_polling(timeout=60, allowed_updates=["message", "photo"])
    
    asyncio.run(main())