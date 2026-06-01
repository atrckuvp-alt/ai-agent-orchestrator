import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
# --- หลังจากนั้นด้านล่างปล่อยให้เป็นโค้ดเดิมของคุณปกติได้เลยครับ ---
import logging
# ตัวอย่างโค้ดเดิมของคุณ...
import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
# ✨ เปลี่ยนมาเรียกใช้ตัวแปรคลาสอัจฉรียะที่เราทำไว้ในข้อ 1
from intent_router import intent_router

# เพิ่มการ Import สำหรับ Web Server หลอกระบบ Render
from fastapi import FastAPI
import uvicorn

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ALLOWED_USERS = [7238952711] # ← เปลี่ยนเป็น ID ของคุณ

user_states = {}

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# Import
# หมายเหตุ: ตรวจสอบให้แน่ใจว่าไฟล์เหล่านี้อยู่ในโฟลเดอร์เดียวกันหรือมีใน Path
from meta_orchestrator import MetaOrchestrator
from teams.infrastructure_team import infrastructure_team
from workflow_builder import execute_user_objective, approve_workflow, reject_workflow

meta_orchestrator = MetaOrchestrator()
# ====================== FASTAPI SETUP ======================
# สร้างเว็บเซิร์ฟเวอร์ขนาดเล็กเพื่อตอบสเตตัสให้กับ Health Check ของ Render
app = FastAPI()

@app.get("/")
async def health_check():
    return {
        "status": "healthy", 
        "message": "Conversational AI Command Center is active!",
        "platform": "Render Free Tier"
    }

# ====================== COMMANDS ======================

@dp.message(Command("start", "menu", "help"))
async def cmd_start(message: Message):
    await show_main_menu(message)

async def show_main_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Run Orchestrator", callback_data="run_orchestrator")],
        [InlineKeyboardButton(text="🔬 Research OSS Tools", callback_data="research_oss")],
        [InlineKeyboardButton(text="📋 List Active Teams", callback_data="list_teams")],
        [InlineKeyboardButton(text="📊 System Status", callback_data="status")],
        [InlineKeyboardButton(text="❓ Help", callback_data="help")]
    ])
    await message.answer(
        "🌐 **AI Operations Console**\n"
        "Meta Orchestrator + Core Skills Ready\n"
        "พร้อมใช้งานตามหลักพุทธ + วิมังสา",
        reply_markup=keyboard
    )

# ====================== CALLBACK ======================

@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    data = callback.data

    if data == "run_orchestrator":
        await callback_run_orchestrator(callback.message)
    elif data == "research_oss":
        await callback.message.answer("🔍 กรุณาพิมพ์สิ่งที่ต้องการวิจัย เช่น 'open source tools สำหรับ AI'")
    elif data == "list_teams":
        await list_active_teams(callback.message)
    elif data == "status":
        await show_system_status(callback.message)
    elif data == "help":
        await show_help(callback.message)

    await callback.answer()

async def show_help(message: Message):
    help_text = """
**🆘 คู่มือการใช้งาน AI Orchestrator**

/menu - เปิดเมนูหลัก
/run - รัน Orchestrator
วิจัย... - วิจัย Open Source Tools

**คำสั่งพิเศษ:**
• วิจัย open source tools
• สร้างทีมพัฒนาเว็บ
• รัน full system analysis

**หลักการทำงาน:**
ระบบใช้ Meta Orchestrator วิเคราะห์ตามหลัก
Systems Thinking + ไตรลักษณ์ + อิทธิบาท 4
    """
    await message.answer(help_text)

# ====================== NATURAL LANGUAGE ======================

# แก้ไขเพิ่มการอิมพอร์ตตัวคัดกรองระบบใหม่ไว้ด้านบนของไฟล์ telegram_bot.py ด้วยครับ
# from intent_router import intent_router

@dp.message()
async def handle_message(message: Message):
    if not is_allowed(message.from_user.id):
        return

    user_id = message.from_user.id
    text = message.text

    # 1. Hard Rule: ดักคีย์เวิร์ดล้างสมองเบื้องต้นโดยไม่ใช้ Token AI
    if any(k in text.lower() for k in ["เริ่มใหม่", "ล้างสมอง", "ลบความจำ", "reset"]):
        user_memory.clear_memory(user_id)
        await message.answer("🧹 ระบบคัดกรองทำการล้างความจำเก่าให้เรียบร้อยแล้วครับ สามารถเริ่มต้นคุยหัวข้อใหม่ได้เลย")
        return

    # 2. เรียกใช้งานตัวคัดกรองเจตนาผูกความจำที่เราสร้างขึ้น (ตาม intent_routing.md)
    await message.answer("🧠 กำลังวิเคราะห์เจตนาและตรวจสอบบริบทความจำ...")
    intent_result = await intent_router.route_intent_with_memory(text, user_id=user_id)
    
    intent_name = intent_result.get("intent", "show_menu")
    combined_objective = intent_result.get("objective", text)

    # 3. แตกแขนงการทำงานตามคำสั่ง Intent ID 01 - 04
    if intent_name == "oss_research":
        await message.answer("🔬 [Intent: OSS Research] กำลังส่งต่อข้อมูลให้ Infrastructure Team วิจัย...")
        result = await execute_user_objective(combined_objective, user_id=user_id)
        await message.answer(result.get("message"))

    elif intent_name == "cost_optimization":
        await message.answer("💰 [Intent: Cost Optimization] กำลังประเมินและวิเคราะห์คำนวณต้นทุนระบบ...")
        result = await execute_user_objective(f"วิเคราะห์เรื่องการประหยัดต้นทุน: {combined_objective}", user_id=user_id)
        await message.answer(result.get("message"))

    elif intent_name == "run_orchestrator":
        await message.answer("🚀 [Intent: Run Orchestrator] เปิดระบบประมวลผลเพื่อตรวจสอบ AI Model...")
        result = await execute_user_objective(combined_objective, user_id=user_id)
        await message.answer(result.get("message"))

    elif intent_name == "show_menu":
        # กรณีขอดูเมนู หรือ AI วิเคราะห์แล้วไม่เข้าพวก
        await show_main_menu(message)

    else:
        await show_main_menu(message)

# ====================== MAIN (Refactored) ======================
async def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # ดึงค่าพอร์ตที่ Render มอบให้ผ่าน Environment Variable (หากไม่มีจะใช้ 8080)
    port = int(os.getenv("PORT", 8080))
    
    # ตั้งค่าคอนฟิกสำหรับ Uvicorn เพื่อรัน FastAPI Web Server
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)

    logger.info("🤖 Starting Telegram AI Operations Platform + FastAPI Server...")
    
    # ใช้ asyncio.gather เพื่อเปิด Web Server หลอก Render ไปพร้อม ๆ กับการทำ Polling บอต 
    await asyncio.gather(
        server.serve(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped cleanly.")