import os
import sys
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from meta_orchestrator import meta_orchestrator
from user_memory import user_memory

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("❌ ERROR: ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables!")
    sys.exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    """รองรับคำสั่ง /start และแนะนำตัว"""
    welcome_text = (
        "🤖 **ยินดีต้อนรับสู่ AI Command Center (STEP 26) ครับนายท่าน!**\n\n"
        "ผมได้รับการอัปเกรดระบบผสานคำสั่งคู่ขนาน (Multi-Team Integration) เรียบร้อยแล้ว\n"
        "ท่านสามารถพิมพ์สั่งงานให้วิจัยระบบอินฟรา หรือ ค้นหาซอฟต์แวร์ Open-Source ได้ทันทีครับ!"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message()
async def handle_nlp_command(message: types.Message):
    """
    [LAYER 1 - Telegram Interface Layer with Response Integration]
    รับข้อความ NLP, ส่งเข้าตัวจัดสรรทีมย่อย และดึงข้อมูลผลลัพธ์กลับมาแสดงผลให้ผู้ใช้
    """
    user_id = message.from_user.id
    user_text = message.text.strip()
    
    print(f"📥 [Webhook Working!] Processing Natural Language from {user_id}: '{user_text}'")
    
    # 1. แจ้งเตือนผู้ใช้ว่าระบบรับเรื่องแล้ว และกำลังประมวลผลผ่าน Workflow Builder
    progress_msg = await message.answer(
        f"⏳ **[Dynamic Workflow]** กำลังจัดสรรทีมงานวิจัยหัวข้อ: *'{user_text}'* ...",
        parse_mode="Markdown"
    )

    try:
        # 2. ส่งต่อให้ MetaOrchestrator สับสายงานและรันโมดูลทีมย่อย
        execution_result = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
        
        # 3. ตรวจสอบและผสานการตอบกลับ (Response Integration Parsing)
        if execution_result.get("status") == "success":
            payload = execution_result.get("data", {})
            
            # ถ้าเป็น General Chat ที่ Orchestrator ตอบกลับข้อความคำแนะนำมาแล้ว
            if isinstance(payload, dict) and "message" in payload:
                await progress_msg.edit_text(payload["message"], parse_mode="Markdown")
                return

            # กรณีผลลัพธ์มาจากทีมปฏิบัติการย่อย (คืนค่ากลับมาเป็นรูปแบบรายงาน)
            if "result" in payload:
                report_data = payload["result"]
                
                # ตรวจสอบว่าเป็นรูปแบบรายงานของ OSS Research Team
                if "best_tools" in report_data:
                    formatted_report = f"🛰️ **[OSS Research Team Report]**\n" \
                                       f"หมวดหมู่ซอฟต์แวร์: *{report_data.get('category')}*\n\n" \
                                       f"🌟 **เครื่องมือ Open-Source ที่แนะนำ:**\n"
                    
                    for idx, tool in enumerate(report_data.get("best_tools", []), 1):
                        formatted_report += f"{idx}️⃣ **{tool['name']}**\n" \
                                            f"• จุดเด่น: _{tool['benefits']}_\n" \
                                            f"• GitHub: `{tool['github_stars']}`\n\n"
                                            
                    formatted_report += f"💡 **บทสรุปจากทีมวิจัย:**\n`{report_data.get('conclusion')}`"
                    await progress_msg.edit_text(formatted_report.strip(), parse_mode="Markdown")
                else:
                    # กรณีเป็นผลลัพธ์จากทีมอื่น (เช่น Infrastructure Team) ที่ไม่มีโครงสร้าง best_tools
                    await progress_msg.edit_text(
                        f"✅ **[Task Completed]** ระบบประมวลผลแผนงานอินฟราเรียบร้อยแล้วครับนายท่าน! ผลลัพธ์ถูกบันทึกลงคลังความจำเรียบร้อย", 
                        parse_mode="Markdown"
                    )
            else:
                await progress_msg.edit_text("✅ ระบบบันทึกและประมวลผลคำสั่งสำเร็จเรียบร้อยครับ!")
                
        elif execution_result.get("status") == "failed":
            await progress_msg.edit_text(f"⚠️ {execution_result.get('message')}")
            
        else:
            # Handling Fallback Actions
            await progress_msg.edit_text(f"💡 {execution_result.get('message')}")

    except Exception as e:
        print(f"❌ [Telegram Bot Runtime Error] {e}")
        await progress_msg.edit_text(f"💥 เกิดข้อผิดพลาดในระบบแชท: `{e}`", parse_mode="Markdown")

async def main():
    print("🤖 [Telegram Bot] Starting polling services for STEP 26 Multi-Team Response Integration...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())