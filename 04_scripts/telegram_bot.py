# Complete file: 04_scripts/telegram_bot.py (With Integrated Chronos A & Vision B)
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

# =====================================================================
# ⏰ [PLAN A - CORE CHRONOS WATCHER] 
# =====================================================================
async def autonomous_cron_loop(bot_instance, target_user_id: int):
    print("⏳ [Chronos Watcher] ระบบตรวจเช็คเวลาอัตโนมัติเปิดใช้งานคู่ขนานแล้ว...")
    has_run_today = False
    
    while True:
        try:
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
            if now.hour == 9 and now.minute == 0:
                if not has_run_today:
                    print("🔔 [Chronos Trigger] ได้เวลา 09:00 น. สั่งเดินเครื่องรายงานประจำวัน!")
                    await bot_instance.send_message(
                        chat_id=target_user_id, 
                        text="⏰ **[Morning Briefing]** อรุณสวัสดิ์ครับนายท่าน! ระบบเริ่มประมวลผลรายงานยุทธศาสตร์ประจำวันอัตโนมัติแล้วครับ..."
                    )
                    scheduled_result = await meta_orchestrator.execute_scheduled_task(user_id=target_user_id)
                    
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
                if now.hour != 9 or now.minute != 0:
                    has_run_today = False
                    
            await asyncio.sleep(30)
        except Exception as cron_err:
            print(f"⚠️ [Chronos Warning] ลูปตรวจเวลาติดขัดเล็กน้อย: {cron_err}")
            await asyncio.sleep(60)

# =====================================================================
# 👁️ [PLAN B - TELEGRAM PHOTO GATEWAY RECEIVER]
# =====================================================================
@bot.message_handler(content_types=['photo'])
async def handle_incoming_photo(message):
    """
    [STEP 33 - Photo Handler] 
    ดักจับเมื่อนายท่านแคปหน้าจอ Error หรือผังระบบส่งเข้ามาในแชท
    """
    user_id = message.from_user.id
    caption = message.caption if message.caption else ""
    
    print(f"📸 [Photo Received] ได้รับไฟล์ภาพจาก User ID {user_id} พร้อมคำอธิบาย: {caption}")
    
    try:
        # แจ้งสถานะให้นายท่านอุ่นใจก่อน
        await bot.reply_to(message, "👁️ **[Vision Scanner]** ได้รับไฟล์ภาพของนายท่านแล้วครับ กำลังเปิดดวงตาสแกนพิมพ์เขียวและรายละเอียดหลังบ้านสักครู่...")
        
        # ดึงไฟล์ภาพขนาดใหญ่ที่สุดจากอาร์เรย์ที่ส่งมา
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        
        # บันทึกภาพลงโฟลเดอร์ชั่วคราวในโปรเจกต์อย่างปลอดภัย
        temp_dir = ROOT / "00_memory" / "temp_images"
        temp_dir.mkdir(parents=True, exist_ok=True)
        image_save_path = temp_dir / f"vision_{message.photo[-1].file_id}.jpg"
        image_save_path.write_bytes(downloaded_file)
        
        # ส่งภาพไปให้สมองใหญ่ MetaOrchestrator วิเคราะห์ผ่านโมเดลสายตาคมกริบ
        vision_response = await meta_orchestrator.route_and_execute_vision(
            image_path=str(image_save_path), 
            caption_text=caption, 
            user_id=user_id
        )
        
        # ส่งคำตอบกลับไปบอกนายท่าน
        if vision_response and "data" in vision_response and "message" in vision_response["data"]:
            await bot.send_message(chat_id=message.chat.id, text=vision_response["data"]["message"])
            
        # ลบไฟล์ทิ้งหลังใช้งานเสร็จเพื่อเคลียร์พื้นที่เซิฟเวอร์ให้เบาสบาย
        if image_save_path.exists():
            image_save_path.unlink()
            
    except Exception as e_photo:
        print(f"💥 [Photo Processing Error] การประมวลผลภาพล้มเหลว: {e_photo}")
        await bot.send_message(chat_id=message.chat.id, text="⚠️ เกิดข้อผิดพลาดทางเทคนิคในการประมวลผลไฟล์ภาพตัวนี้ครับพ้ม")

# =====================================================================
# 💬 [TELEGRAM MESSAGES GATEWAY LOGIC]
# =====================================================================
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    welcome_text = (
        "🤖 **ยินดีต้อนรับสู่ AI Command Center (v2.0)**\n\n"
        "⏰ แผน A: ตั้งเวลาส่งรายงานเช้าอัตโนมัติ (Active)\n"
        "👁️ แผน B: ดวงตาสแกนผังระบบและภาพพิมพ์เขียว (Active)\n\n"
        "🛡️ *คุ้มครองความปลอดภัยระบบด้วยมหาเกราะสับสาย 5 ชั้น ไร้ค่าใช้จ่ายร้อยเปอร์เซ็นต์*"
    )
    await bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    user_id = message.from_user.id
    user_text = message.text
    
    print(f"📥 [Incoming Message] จาก User ID {user_id}: {user_text}")
    orchestrator_response = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
    
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
    MY_USER_ID = 7238952711
    asyncio.create_task(autonomous_cron_loop(bot_instance=bot, target_user_id=MY_USER_ID))
    
    print("📡 [Polling Active] เชื่อมต่อสัญญาณรอรับภาพและข้อความ 24 ชั่วโมง...")
    await bot.infinity_polling(timeout=60, allowed_updates=["message", "photo"])

if __name__ == "__main__":
    asyncio.run(main())