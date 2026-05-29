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

# Import Meta Orchestrator
from meta_orchestrator import meta_orchestrator
from workflow_builder import execute_user_objective, approve_workflow, reject_workflow

# ====================== NATURAL LANGUAGE PARSER ======================

async def parse_user_intent(text: str):
    """Natural Language Parser ที่ดีขึ้น"""
    lower = text.lower()
    
    if any(word in lower for word in ["รัน", "run", "เริ่ม", "execute", "สั่งงาน", "สั่ง"]):
        return {"intent": "run_orchestrator", "objective": text}
    
    if any(word in lower for word in ["สร้างทีม", "สร้าง team", "team", "สร้าง ai"]):
        return {"intent": "create_team", "objective": text}
    
    if any(word in lower for word in ["วิจัย", "หา", "analyze", "research", "ศึกษ"]):
        return {"intent": "research_task", "objective": text}
    
    if any(word in lower for word in ["พัฒนา", "coding", "build", "เขียนโค้ด", "โปรแกรม"]):
        return {"intent": "coding_task", "objective": text}
    
    return {"intent": "general", "objective": text}

# ====================== MAIN MENU ======================

async def show_main_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Run Orchestrator", callback_data="run_orchestrator")],
        [InlineKeyboardButton(text="🛠️ Create New Team", callback_data="create_team")],
        [InlineKeyboardButton(text="📋 List Active Teams", callback_data="list_teams")],
        [InlineKeyboardButton(text="📊 System Status", callback_data="status")]
    ])
    await message.answer("🌐 **AI Operations Console**", reply_markup=keyboard)

async def show_team_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔬 Research", callback_data="team_research")],
        [InlineKeyboardButton(text="💻 Coding", callback_data="team_coding")],
        [InlineKeyboardButton(text="⚡ Full Stack", callback_data="team_fullstack")]
    ])
    await message.answer("🛠️ **เลือกประเภททีม AI**", reply_markup=keyboard)

async def show_mode_menu(message: Message, user_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧪 Mock Mode", callback_data="mode_mock")],
        [InlineKeyboardButton(text="🚀 Real API Mode", callback_data="mode_real")]
    ])
    await message.answer("⚙️ **เลือกโหมดการทำงาน**", reply_markup=keyboard)

# ====================== CALLBACK HANDLERS ======================

@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    data = callback.data

    if data == "run_orchestrator":
        await callback.message.answer("🧠 Meta Orchestrator กำลังวิเคราะห์...")
        routing = meta_orchestrator.route_objective("Run full system analysis")
        result = await execute_user_objective(routing['objective'], mode="mock")
        if result["success"]:
            await send_approval_request(callback.message, result["workflow_id"], result["objective"])

    elif data.startswith("approve_"):
        workflow_id = data.replace("approve_", "")
        await callback.message.edit_text(f"✅ กำลังอนุมัติ Workflow `{workflow_id}`...")
        result = await approve_workflow(workflow_id)
        await callback.message.answer(f"✅ {result.get('message', 'Approved!')}")

    elif data.startswith("reject_"):
        workflow_id = data.replace("reject_", "")
        await callback.message.edit_text(f"❌ Workflow `{workflow_id}` ถูกปฏิเสธ")
        result = await reject_workflow(workflow_id, "Rejected by user via Telegram")
        await callback.message.answer("✅ ปฏิเสธ Workflow เรียบร้อยแล้ว")

    elif data == "list_teams":
        await list_active_teams(callback.message)

    elif data == "create_team":
        await show_team_menu(callback.message)

    elif data == "status":
        await show_system_status(callback.message)

    await callback.answer()

async def send_approval_request(message: Message, workflow_id: str, objective: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Approve", callback_data=f"approve_{workflow_id}"),
            InlineKeyboardButton(text="❌ Reject", callback_data=f"reject_{workflow_id}")
        ]
    ])
    await message.answer(
        f"📋 **Workflow ต้องการการอนุมัติ**\n\n"
        f"**ID:** `{workflow_id}`\n"
        f"**Objective:** {objective[:150]}...\n\n"
        "กรุณาตัดสินใจ:",
        reply_markup=keyboard
    )

async def list_active_teams(message: Message):
    await message.answer("📋 List Active Teams (กำลังพัฒนาเต็มรูปแบบ...)")

async def show_system_status(message: Message):
    await message.answer("📊 **System Status**\n✅ Meta Orchestrator: Active\n✅ Natural Language: Ready")

# ====================== MESSAGE HANDLER ======================

@dp.message()
async def handle_message(message: Message):
    if not is_allowed(message.from_user.id):
        return

    user_text = message.text.strip()
    user_id = message.from_user.id

    # ตรวจสอบสถานะการสนทนา
    state = user_states.get(user_id)
    if state and state.get("step") == "waiting_objective":
        user_states[user_id]["objective"] = user_text
        user_states[user_id]["step"] = "waiting_mode"
        await show_mode_menu(message, user_id)
        return

    intent = await parse_user_intent(user_text)

    if intent["intent"] == "run_orchestrator":
        await callback_run_orchestrator(message)
    elif intent["intent"] == "create_team":
        await callback_create_team(message, intent)
    else:
        await show_main_menu(message)

async def callback_run_orchestrator(message: Message):
    await message.answer("🧠 Meta Orchestrator กำลังวิเคราะห์...")
    routing = meta_orchestrator.route_objective(message.text)
    result = await execute_user_objective(routing['objective'], mode="mock")
    if result["success"]:
        await send_approval_request(message, result["workflow_id"], result["objective"])

async def callback_create_team(message: Message, intent):
    await show_team_menu(message)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 Telegram AI Operations Bot + Improved Natural Language is running...")
    await dp.start_polling(bot)

# ====================== HEALTH CHECK SERVER ======================
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"AI Orchestrator Bot is running on Render.com")
        return

def run_health_server():
    """รัน Health Check Server บน port 10000"""
    try:
        server = HTTPServer(('0.0.0.0', 10000), HealthHandler)
        print("🌐 Health check server started on port 10000")
        server.serve_forever()
    except Exception as e:
        print(f"⚠️ Health server failed to start: {e}")

# ====================== MAIN ======================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 Telegram AI Operations Platform is starting...")

    # รัน Health Server ใน Thread แยก
    health_thread = Thread(target=run_health_server, daemon=True)
    health_thread.start()

    print("🌐 Health check server is running (port 10000)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())