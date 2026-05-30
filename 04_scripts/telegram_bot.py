import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
import os
from pathlib import Path

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
from meta_orchestrator import meta_orchestrator
from teams.infrastructure_team import infrastructure_team
from workflow_builder import execute_user_objective, approve_workflow, reject_workflow

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

async def parse_user_intent(text: str):
    lower = text.lower().strip()
    if any(k in lower for k in ["วิจัย", "research", "หา tool", "oss"]):
        return {"intent": "research_task", "objective": text}
    if any(k in lower for k in ["รัน", "run", "เริ่ม", "execute", "orchestrator"]):
        return {"intent": "run_orchestrator", "objective": text}
    return {"intent": "general", "objective": text}

@dp.message()
async def handle_message(message: Message):
    if not is_allowed(message.from_user.id):
        return

    intent = await parse_user_intent(message.text)

    if intent["intent"] == "research_task":
        await message.answer("🔍 Infrastructure Team กำลังวิจัย...")
        result = await infrastructure_team.research_open_source(intent["objective"])
        await message.answer(f"✅ วิจัยเสร็จสิ้น\n**Category:** {result.get('category')}\n**Status:** {result.get('status')}")
    elif intent["intent"] == "run_orchestrator":
        await callback_run_orchestrator(message)
    else:
        await show_main_menu(message)

# ====================== MAIN ======================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 Telegram AI Operations Platform + Final Polish is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())