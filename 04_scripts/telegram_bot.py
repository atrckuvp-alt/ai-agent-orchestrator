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

# =====================================================================
# 📍 ค้นหาฟังก์ชัน @dp.message() ของเก่า แล้วแทนที่ด้วยโค้ดด้านล่างนี้ทั้งหมด
# =====================================================================

@dp.message()
async def handle_text_message(message: Message):
    user_id = message.from_user.id
    if not is_allowed(user_id):
        await message.answer("❌ คุณไม่มีสิทธิ์ใช้งานระบบนี้")
        return

    text = message.text
    logger.info(f"📥 [Telegram Bot] Received message from {user_id}: {text}")

    # 🔗 [แทรกจุดที่ 1.1] บันทึกข้อความของผู้ใช้เข้าสู่ Short-Term Buffer ทันทีที่รับมา
    try:
        from memory_manager import memory_manager
        memory_manager.add_to_short_term(user_id, role="user", content=text)
    except Exception as e:
        logger.error(f"⚠️ [Memory Error] ไม่สามารถเพิ่มข้อความลงบัฟเฟอร์ได้: {e}")

    # --- (ส่วนนี้คือโค้ดประมวลผล Intent เดิมของคุณ) ---
    route_res = await intent_router.route_intent_with_memory(text, user_id=user_id)
    intent_name = route_res.get("intent", "general")
    combined_objective = route_res.get("objective", text)

    ai_reply_text = "" # ตัวแปรสำหรับดักเก็บคำตอบสุดท้ายส่งไปลงความจำ

    if intent_name == "oss_research":
        await message.answer("🔍 [Intent: OSS Research] กำลังค้นหาข้อมูล Open-source...")
        result = await execute_user_objective(f"วิเคราะห์ตัวเลือก Open-source: {combined_objective}", user_id=user_id)
        ai_reply_text = result.get("message", "")
        await message.answer(ai_reply_text)

    elif intent_name == "cost_optimization":
        await message.answer("💰 [Intent: Cost Optimization] กำลังวิเคราะห์งบประมาณและทรัพยากร...")
        result = await execute_user_objective(f"วิเคราะห์แนวทางการประหยัดต้นทุน: {combined_objective}", user_id=user_id)
        ai_reply_text = result.get("message", "")
        await message.answer(ai_reply_text)

    elif intent_name == "run_orchestrator":
        await message.answer("🚀 [Intent: Run Orchestrator] เปิดระบบประมวลผลเพื่อตรวจสอบ AI Model...")
        result = await execute_user_objective(combined_objective, user_id=user_id)
        ai_reply_text = result.get("message", "")
        await message.answer(ai_reply_text)

    elif intent_name == "show_menu":
        await show_main_menu(message)
    else:
        # 🧠 [จุดแทรกโค้ดใหม่] จัดการข้อความทั่วไป (General Chat) ป้องกันบอทนิ่งเงียบ
        # เช็คว่าถ้าตัวแปร ai_reply_text ยังว่างอยู่ (เพราะ AI ไม่ได้เจนอะไรกลับมา) ให้ใส่ข้อความต้อนรับแทน
        if not ai_reply_text or ai_reply_text.strip() == "":
            ai_reply_text = f"🤖 สวัสดีครับนายท่าน! ผมรับทราบข้อความ '{text}' เรียบร้อยแล้ว ปัจจุบันระบบกำลังเตรียมพร้อมเข้าสู่สเต็ปถัดไป (STEP 26) หากต้องการสั่งงานด่วน สามารถใช้คำสั่งผ่านเมนูหลักได้เลยครับ!"
        
        # ส่งข้อความตอบกลับผู้ใช้ใน Telegram ทันที
        await message.answer(ai_reply_text)

    # 🔗 [แทรกจุดที่ 1.2] เมื่อ AI ทำงานเสร็จและตอบผู้ใช้แล้ว บันทึกคำตอบและสั่งสรุปความจำระยะยาว
    if ai_reply_text:
        try:
            # 1. บันทึกคำตอบของ AI ลง Short-Term Buffer
            memory_manager.add_to_short_term(user_id, role="assistant", content=ai_reply_text)
            
            # 2. คอนแว่นต์/บีบอัดข้อมูลเป็นประสบการณ์สะสมระยะยาว (คำนวณผ่านโมเดลฟรี ทริกเกอร์ Async)
            logger.info("🧠 [Memory System] เริ่มทำการสกัดประสบการณ์และคีย์เวิร์ดสำคัญ...")
            await memory_manager.compress_and_update_long_term(user_id)
            logger.info("✅ [Memory System] ซิงค์ความจำระยะยาวขึ้นคลาวด์/ดิสก์ เรียบร้อยแล้ว")
        except Exception as e:
            logger.error(f"⚠️ [Memory Management Engine Error]: {e}")

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