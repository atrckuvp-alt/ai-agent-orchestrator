# Complete file: 04_scripts/telegram_bot.py (With Autonomous Cron Scheduler)
import os
import sys
import asyncio
import datetime
from pathlib import Path
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

# เซ็ตอัพ Path เพื่อให้มองเห็นโมดูลร่วมกันได้
CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# โหลดค่าคอนฟิกูเรชันจาก .env
load_dotenv(dotenv_path=ROOT / ".env")

from meta_orchestrator import meta_orchestrator

# เรียกใช้งาน Token จากระบบความปลอดภัย คอนฟิกผ่าน Render Dashboard
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("💥 ไม่พบ TELEGRAM_BOT_TOKEN ในระบบ Environment Variables!")

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

# =====================================================================
# ⏰ [PLAN A - CORE CHRONOS WATCHER] 
# =====================================================================
async def autonomous_cron_loop(bot_instance, target_user_id: int):
    """
    [STEP 32 - Background Clock Watcher]
    ลูปเฝ้าระวังเวลาโลก รันเงียบๆ หลังบ้าน กินทรัพยากร 0%
    ล็อกเป้าหมายเวลาไทยในการเสิร์ฟรายงานสรุปยุทธศาสตร์ประจำวัน
    """
    print("⏳ [Chronos Watcher] ระบบตรวจเช็คเวลาอัตโนมัติเปิดใช้งานคู่ขนานแล้ว...")
    has_run_today = False
    
    while True:
        try:
            # ดึงเวลาปัจจุบันและปรับฐานเป็นเวลาประเทศไทย (GMT+7) เพื่อรองรับเซิฟเวอร์ Render นอก
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
            
            # 🔔 ตั้งเวลาเดินเครื่อง: สแตนด์บายที่เวลา 09:00 น. ของทุกวัน (ปรับเปลี่ยนได้ตามชอบใจครับ)
            if now.hour == 9 and now.minute == 0:
                if not has_run_today:
                    print("🔔 [Chronos Trigger] ได้เวลา 09:00 น. สั่งเดินเครื่องรายงานประจำวัน!")
                    
                    # 1. ส่งสารแจ้งเตือนเปิดม่านอรุณสวัสดิ์ทักทายนายท่านใน Telegram
                    await bot_instance.send_message(
                        chat_id=target_user_id, 
                        text="⏰ **[Morning Briefing]** อรุณสวัสดิ์ครับนายท่าน! ระบบเริ่มประมวลผลรายงานยุทธศาสตร์ประจำวันอัตโนมัติแล้วครับ..."
                    )
                    
                    # 2. ส่งคำสั่งยุทธวิธีเข้าศูนย์ควบคุมสั่งการผ่านเกราะ 5 ชั้น
                    scheduled_result = await meta_orchestrator.execute_scheduled_task(user_id=target_user_id)
                    
                    # 3. นำผลลัพธ์ที่ได้ส่งสรุปปิดจ๊อบสวยๆ กลับไปให้นายท่าน
                    if scheduled_result and "data" in scheduled_result and "result" in scheduled_result["data"]:
                        report = scheduled_result["data"]["result"]
                        conclusion = report.get("conclusion", "ประมวลผลเสร็จสิ้นสมบูรณ์")
                        best_tools = report.get("best_tools", [{}])[0].get("name", "AI Infrastructure")
                        
                        await bot_instance.send_message(
                            chat_id=target_user_id,
                            text=f"🏆 **[Strategic Report Summary]**\n\n🎯 **หัวข้อสำคัญ:** เทรนด์สถาปัตยกรรมและเครื่องมือที่น่าสนใจ\n🛠️ **เครื่องมือเด่นวันนี้:** {best_tools}\n📝 **สรุปใจความ:** {conclusion}\n\n🛡️ *รายงานส่งอัตโนมัติผ่านขุมพลังมหาเกราะป้องกัน 5 ชั้น*"
                        )
                    
                    has_run_today = True
            else:
                # รีเซ็ตตัวแปรล็อกเพื่อรอรันวันถัดไปเมื่อพ้นนาทีที่กำหนด
                if now.hour != 9 or now.minute != 0:
                    has_run_today = False
                    
            # หลับพักผ่อนชั่วคราว 30 วินาทีเพื่อการประหยัดสเปคหลังบ้าน
            await asyncio.sleep(30)
            
        except Exception as cron_err:
            print(f"⚠️ [Chronos Warning] ลูปตรวจเวลาติดขัดเล็กน้อย: {cron_err}")
            await asyncio.sleep(60)


# =====================================================================
# 💬 [TELEGRAM MESSAGES GATEWAY LOGIC]
# =====================================================================
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    welcome_text = (
        "🤖 **ยินดีต้อนรับสู่ AI Command Center (v1.5)**\n\n"
        "ระบบตอบกลับและวางกลยุทธ์ทางเทคโนโลยีผ่านสถาปัตยกรรมมหาเกราะป้องกัน 5 ชั้น พร้อมระบบตั้งเวลาทำงานอัตโนมัติ (Plan A) เปิดใช้งานแล้วครพพ้ม!"
    )
    await bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    user_id = message.from_user.id
    user_text = message.text
    
    print(f"📥 [Incoming Message] จาก User ID {user_id}: {user_text}")
    
    # ส่งต่อข้อความเข้าสู่ MetaOrchestrator เพื่อประมวลผลสลับสายหา LLM ที่พร้อม
    orchestrator_response = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
    
    # ตรวจสอบและดึงข้อความกลับไปตอบในแชทกลุ่มหรือแชทส่วนตัว Telegram
    if orchestrator_response and "data" in orchestrator_response:
        data_payload = orchestrator_response["data"]
        
        if "message" in data_payload:
            await bot.send_message(chat_id=message.chat.id, text=data_payload["message"])
        elif "result" in data_payload:
            result_core = data_payload["result"]
            conclusion = result_core.get("conclusion", "ดำเนินการเรียบร้อยครับนายท่าน")
            await bot.send_message(chat_id=message.chat.id, text=f"📋 **[ผลการวิเคราะห์]**\n\n{conclusion}")


# =====================================================================
# 🚀 [CORE RUNTIME MAIN FUNCTION]
# =====================================================================
async def main():
    print("🚀 [Bot Ignition] กำลังเปิดเครื่องระบบส่งสารหลักทาง Telegram...")
    
    # 🔥 ผูกนาฬิกาปลุกเลขาฯ ส่วนตัว (Plan A Background Task) เข้าลูปหลัก
    # ล็อกเป้าหมาย ID ของนายท่านโดยตรงเพื่อเสิร์ฟงานตอนเช้าอย่างแม่นยำ
    MY_USER_ID = 7238952711
    asyncio.create_task(autonomous_cron_loop(bot_instance=bot, target_user_id=MY_USER_ID))
    
    print("📡 [Polling Active] เชื่อมต่อสัญญาณรอรับฟังคำสั่งนายท่าน 24 ชั่วโมง...")
    await bot.infinity_polling(timeout=60, allowed_updates=["message"])

if __name__ == "__main__":
    # รันลูปเหตุการณ์หลักแบบอิงโครงสร้าง Asyncio เต็มรูปแบบ
    asyncio.run(main())