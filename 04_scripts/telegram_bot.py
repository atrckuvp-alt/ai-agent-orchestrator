import os
import sys
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Update
from contextlib import asynccontextmanager
from pathlib import Path

# ค้นหาพาธรากฐานของโปรเจกต์หลัก
CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from meta_orchestrator import meta_orchestrator
from user_memory import user_memory

# 1. ตรวจสอบโทเค็นความปลอดภัยในการเชื่อมต่อกับ Telegram API
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    print("❌ ERROR: ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables!")
    sys.exit(1)

# 2. ตั้งค่าคลาสควบคุมเหตุการณ์ของบอท
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ----------------- [HANDLER LAYER] -----------------

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    """รองรับคำสั่งเริ่มต้นเปิดแอป /start"""
    welcome_text = (
        "🤖 **ยินดีต้อนรับสู่ AI Command Center (STEP 26) ครับนายท่าน!**\n\n"
        "ผมได้รับการอัปเกรดระบบผสานผลลัพธ์ข้อมูลและสลับสายการรันงานเรียบร้อยแล้ว\n"
        "ท่านสามารถพิมพ์สั่งงานให้วิจัยระบบอินฟรา หรือ ค้นหาซอฟต์แวร์ Open-Source ได้เลยครับ!"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message()
async def handle_nlp_command(message: types.Message):
    """
    [LAYER 1 - Telegram Interface Layer with Response Integration]
    รับคำสั่งข้อความปกติ -> ส่งไปแยกสายประมวลผลหลังบ้าน -> ดึงรายงานตอบกลับแบบทันที
    """
    user_id = message.from_user.id
    user_text = message.text.strip()
    
    print(f"📥 [Webhook Working!] Processing Natural Language from {user_id}: '{user_text}'")
    
    # ส่งสัญญาณตอบกลับเบื้องต้นระหว่างจัดเตรียมทีมปฏิบัติการ
    progress_msg = await message.answer(
        f"⏳ **[Dynamic Workflow]** กำลังจัดสรรทีมงานวิจัยหัวข้อ: *'{user_text}'* ...",
        parse_mode="Markdown"
    )

    try:
        # Schedulers สั่งการให้หัวหน้าใหญ่จัดตั้งสายงานปฏิบัติการ
        execution_result = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
        
        # ถอดโครงสร้างและแปลงผลลัพธ์เป็นข้อความรายงานส่งกลับ (Response Integration)
        if execution_result.get("status") == "success":
            payload = execution_result.get("data", {})
            
            # กรณีจับคู่ได้เป็นคำพูดคุยทักทายทั่วไป (General Chat)
            if isinstance(payload, dict) and "message" in payload:
                await progress_msg.edit_text(payload["message"], parse_mode="Markdown")
                return

            # กรณีมาจากทีมปฏิบัติการย่อยที่คืนสถานะเป็น Payload ข้อมูลรายงาน
            if "result" in payload:
                report_data = payload["result"]
                
                # ตรวจพบโครงสร้างรายงานของทีม OSS Research Team
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
                    # กรณีเป็นทีมอื่นๆ เช่น Infrastructure Team
                    await progress_msg.edit_text(
                        f"✅ **[Task Completed]** ระบบประมวลผลสถาปัตยกรรมอินฟราเรียบร้อยแล้วครับนายท่าน! ข้อมูลถูกอัปเดตลงคลังเรียบร้อย", 
                        parse_mode="Markdown"
                    )
            else:
                await progress_msg.edit_text("✅ ระบบบันทึกและประมวลผลคำสั่งสำเร็จเรียบร้อยครับ!")
                
        elif execution_result.get("status") == "failed":
            await progress_msg.edit_text(f"⚠️ {execution_result.get('message')}")
            
        else:
            await progress_msg.edit_text(f"💡 {execution_result.get('message')}")

    except Exception as e:
        print(f"❌ [Telegram Bot Runtime Error] {e}")
        await progress_msg.edit_text(f"💥 เกิดข้อผิดพลาดในระบบแชท: `{e}`", parse_mode="Markdown")

# ----------------- [FASTAPI WEBHOOK LAYER] -----------------

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    ควบคุมขั้นตอนการบูตระบบและปิดตัวของเซิฟเวอร์บน Render
    ทำการสแกนล้างระบบ Polling เก่า และเชื่อมต่อเส้นทาง Webhook ยิงตรงเข้าหาพอร์ตหลัก
    """
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        webhook_path = f"{render_url}/webhook"
        print(f"🚀 [Lifespan Startup] ล้างท่อ Polling เก่า และเชื่อมโยง Webhook ไปที่: {webhook_path}")
        await bot.set_webhook(url=webhook_path, drop_pending_updates=True)
    else:
        print("⚠️ [Lifespan Warning] ไม่พบตัวแปร RENDER_EXTERNAL_URL ระบบอาจรับข้อความผ่าน webhook ไม่ได้")
    
    yield
    # ล้างพอร์ตเชื่อมต่อและเก็บทรัพยากรตอนปิดโปรเจกต์
    await bot.session.close()

# สร้างแอป ASGI (FastAPI) ส่งออกตัวแปร app ให้กับ Uvicorn บน Render โหลดเปิดเว็บเซอร์วิส
app = FastAPI(lifespan=lifespan)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    """ท่อรับแพ็กเก็ตข้อมูลสดๆ ที่ยิงความเคลื่อนไหวมาจากเซิฟเวอร์ Telegram"""
    try:
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        return {"status": "ok"}
    except Exception as e:
        print(f"❌ [Webhook Stream Error] {e}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    return {"status": "online", "message": "AI Command Center is Active!"}