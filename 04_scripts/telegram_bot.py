# Complete file: 04_scripts/telegram_bot.py (Pure FastAPI/ASGI Webhook Integration)
import os
import sys
import asyncio
import datetime
from pathlib import Path
from telebot.types import Update
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

# =====================================================================
# 🌐 [WEBHOOK ENGINE - ASGI APP FOR RENDER]
# =====================================================================
async def app(scope, receive, send):
    """ Fast Webhook Gateway ดักจับข้อมูลที่ Telegram ยิงเข้าทาง POST /webhook """
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                # ตั้งค่าเปิด Chronos Loop คู่ขนานตอนสตาร์ทระบบ
                MY_USER_ID = 7238952711
                asyncio.create_task(autonomous_cron_loop(bot, MY_USER_ID))
                print("📡 [Webhook Active] ระบบสมองกลตั้งรับสัญญาณผ่านท่อ POST /webhook เรียบร้อย...")
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return
                
    elif scope['type'] == 'http' and scope['path'] == '/webhook' and scope['method'] == 'POST':
        # 📥 ดึงข้อมูลดิบ (Body) ที่ Telegram โยนเข้าเซิร์ฟเวอร์
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)
            
        if body:
            try:
                # แปลงข้อมูลดิบเข้าสู่ตัวแปรระบบของ Telebot แล้วสั่งประมวลผลทันที
                json_string = body.decode('utf-8')
                update = Update.de_json(json_string)
                await bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ [Webhook Parse Error] ถอดรหัสคำสั่งพลาด: {e}")
                
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({'type': 'http.response.body', 'body': b'OK'})
        
    else:
        # หน้าแรกแสดงสถานะปกติเมื่อเปิดผ่านเว็บ Browser
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({'type': 'http.response.body', 'body': b'AI Command Center Webhook Status: LIVE'})

# =====================================================================
# ⏰ [PLAN A - CHRONOS WATCHER TIME-ZONE FIXED]
# =====================================================================
async def autonomous_cron_loop(bot_instance, target_user_id: int):
    print("⏳ [Chronos Watcher] ระบบเฝ้าระวังเวลารายงานเช้า เปิดทำงานคู่ขนาน...")
    has_run_today = False
    
    while True:
        try:
            tz_thailand = datetime.timezone(datetime.timedelta(hours=7))
            now = datetime.datetime.now(tz_thailand)
            
            if now.hour == 9 and now.minute == 0:
                if not has_run_today:
                    print("🔔 [Chronos Trigger] ได้เวลา 09:00 น. ยิงรายงานเข้า Telegram!")
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
        "🤖 **AI Command Center (v3.0 - Pure Webhook)**\n\n"
        "🟢 เชื่อมท่อสัญญาณตรงยิงเข้าหน้าเซิร์ฟเวอร์ (Connected)\n"
        "🟢 บังคับฐานเวลาประเทศไทย 09:00 น. (Fixed)\n"
        "🟢 ยูนิต Growth Marketing BU (Ready)"
    )
    await bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    user_id = message.from_user.id
    user_text = message.text
    
    print(f"📥 [Incoming Message via Webhook] จาก {user_id}: {user_text}")
    orchestrator_response = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
    
    if orchestrator_response and "data" in orchestrator_response:
        data_payload = orchestrator_response["data"]
        if "message" in data_payload:
            await bot.send_message(chat_id=message.chat.id, text=data_payload["message"])