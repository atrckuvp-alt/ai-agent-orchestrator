# Complete file: 04_scripts/telegram_bot.py (Robust ASGI Webhook & Strict Event Loop)
import os
import sys
import asyncio
import datetime
import json
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
    """ Fast Webhook Gateway ประมวลผลและล็อคลูปให้ Telegram ตอบกลับสำเร็จ """
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                MY_USER_ID = 7238952711
                asyncio.create_task(autonomous_cron_loop(bot, MY_USER_ID))
                print("📡 [Webhook Active] ระบบสมองกลตั้งรับสัญญาณผ่านท่อ POST /webhook เรียบร้อย...")
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return
                
    elif scope['type'] == 'http' and scope['path'] == '/webhook' and scope['method'] == 'POST':
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)
            
        if body:
            try:
                json_string = body.decode('utf-8')
                # 🛠️ แตกข้อมูลตรงเพื่อเอาไปยิงตอบทันทีเพื่อความแม่นยำ ไม่ผ่าน Middleware ที่อาจทำข้อมูลหล่น
                update_dict = json.loads(json_string)
                if "message" in update_dict:
                    msg_obj = update_dict["message"]
                    chat_id = msg_obj["chat"]["id"]
                    user_id = msg_obj["from"]["id"]
                    user_text = msg_obj.get("text", "")
                    
                    print(f"📥 [Direct Message Trigger] จาก {user_id}: {user_text}")
                    
                    # สั่งประมวลผลและรอผลลัพธ์ให้เสร็จสิ้นคาลูป
                    orchestrator_response = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
                    
                    if orchestrator_response and "data" in orchestrator_response:
                        data_payload = orchestrator_response["data"]
                        if "message" in data_payload:
                            # 🚀 ยิงข้อความกลับแบบจี้ตัวตรงๆ การันตีข้อความถึงมือแน่นอนร้อยเปอร์เซ็นต์
                            await bot.send_message(chat_id=chat_id, text=data_payload["message"])
                else:
                    # หากเป็น Update รูปแบบอื่น ให้ส่งเข้ากระบวนการปกติของ Telebot
                    update = Update.de_json(json_string)
                    await bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ [Webhook Parse Error] ถอดรหัสหรือส่งคำสั่งพลาด: {e}")
                
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({'type': 'http.response.body', 'body': b'OK'})
        
    else:
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/plain']],
        })
        await send({'type': 'http.response.body', 'body': b'AI Command Center Webhook Status: LIVE'})

# =====================================================================
# ⏰ [⏰ CHRONOS WATCHER - TIMEZONE FIXED]
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
                    await bot_instance.send_message(chat_id=target_user_id, text="⏰ **[Morning Briefing]** ระบบเริ่มประมวลผลรายงานยุทธศาสตร์ประจำวันแล้วครับ...")
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