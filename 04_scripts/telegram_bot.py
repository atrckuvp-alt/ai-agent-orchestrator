# นำโค้ดชุดนี้ไปวางทับใน 04_scripts/telegram_bot.py ได้เลยครับเพื่อความเนี๊ยบ
import os
import sys
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Update
from contextlib import asynccontextmanager
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from meta_orchestrator import meta_orchestrator
from user_memory import user_memory

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("❌ ERROR: ไม่พบ TELEGRAM_BOT_TOKEN")
    sys.exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.answer("🤖 **AI Command Center (STEP 27) พร้อมทำงานร่วมกันแบบ Multi-Agent แล้วครับ!**", parse_mode="Markdown")

@dp.message()
async def handle_nlp_command(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text.strip()
    
    progress_msg = await message.answer(
        f"⏳ **[Collaboration Workflow]** กำลังจัดสรรและประสานงานทีมย่อย... *'{user_text}'*",
        parse_mode="Markdown"
    )

    try:
        execution_result = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
        
        if execution_result.get("status") == "success":
            payload = execution_result.get("data", {})
            
            if isinstance(payload, dict) and "message" in payload:
                await progress_msg.edit_text(payload["message"], parse_mode="Markdown")
                return

            if "result" in payload:
                report_data = payload["result"]
                
                if "best_tools" in report_data:
                    formatted_report = f"🛰️ **[OSS Research Team Report]**\n" \
                                       f"หมวดหมู่: *{report_data.get('category')}*\n\n" \
                                       f"🌟 **เครื่องมือ Open-Source ที่แนะนำ:**\n"
                    
                    for idx, tool in enumerate(report_data.get("best_tools", []), 1):
                        formatted_report += f"{idx}️⃣ **{tool['name']}**\n• _{tool['benefits']}_\n"
                                            
                    formatted_report += f"\n💡 **บทสรุปทีม OSS:** `{report_data.get('conclusion')}`\n"
                    
                    # 🤝 ส่วนต่อขยายสเต็ป 27: แสดงรายงานการส่งไม้ต่อให้ทีมอินฟรา
                    if "collaboration_report" in report_data:
                        collab = report_data["collaboration_report"]
                        formatted_report += f"\n" \
                                           f"--- \n\n" \
                                           f"🛡️ **[Cross-Team Handover: {collab['target_team']}]**\n" \
                                           f"📋 **ข้อเสนอแนะด้านสถาปัตยกรรมระบบคลาวด์:**\n" \
                                           f"_{collab['recommendation']}_"
                                           
                    await progress_msg.edit_text(formatted_report.strip(), parse_mode="Markdown")
                else:
                    await progress_msg.edit_text("✅ ระบบประมวลผลแผนงานอินฟราเรียบร้อยแล้ว!")
            else:
                await progress_msg.edit_text("✅ ประมวลผลสำเร็จ!")
    except Exception as e:
        await progress_msg.edit_text(f"💥 ข้อผิดพลาด: `{e}`", parse_mode="Markdown")

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        await bot.set_webhook(url=f"{render_url}/webhook", drop_pending_updates=True)
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    update_data = await request.json()
    update = Update.model_validate(update_data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "online"}