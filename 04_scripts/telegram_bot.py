# Complete file: 04_scripts/telegram_bot.py
import os
import sys
import asyncio
import json
from pathlib import Path
import datetime
from datetime import datetime, timezone, timedelta

# 🔌 [Infra] ระบบล็อกพิกัดจัดเส้นทาง Path ให้รองรับระบบ Linux บน Cloud (Render)
CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent

for path in [str(CURRENT_DIR), str(ROOT)]:
    if path not in sys.path:
        sys.path.insert(0, path)

# โหลดสภาพแวดล้อมสภาพแวดล้อมระบบ (.env)
from dotenv import load_dotenv
load_dotenv(dotenv_path=ROOT / ".env")

# 📥 [Dependencies] โหลดไลบรารีบอทและเซิร์ฟเวอร์ตามหลักเสบียงที่ถูกต้อง
from fastapi import FastAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot

# 🔗 [Modules Link] ดึงตัวแม่การจัดการระบบที่อยู่ด้านนอกมาร่วมวงจร
from meta_orchestrator import meta_orchestrator
from growth_marketing_orchestrator import growth_marketing_orchestrator

# 🤖 [Initialization] ตั้งค่าบอทและแอปพลิเคชันหลัก
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(TOKEN)
app = FastAPI()

# 📂 พิกัดคลังข้อมูลจำลองภายใน
KNOWLEDGE_BASE_PATH = ROOT / "shared_knowledge_base.json"

# =====================================================================
# 📊 [Section 1] ฟังก์ชันแดชบอร์ดสังเกตการณ์ผ่านหน้าเว็บ Portal หลัก
# =====================================================================
def generate_html_dashboard():
    """
    สร้างหน้าเว็บรายงานสถานะ โดยดึงข้อมูลจากไฟล์ความรู้ภายในมาแสดงผล
    """
    db = {}
    if KNOWLEDGE_BASE_PATH.exists():
        with open(KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
            
    insights_list = db.get("insights", [])
    
    # 🎯 แก้ไขท่อนโครงสร้างเวลาไทย คลีนเสร็จสรรพไม่มีเอเรอร์ตัวแดง
    tz_th = timezone(timedelta(hours=7))
    update_time = datetime.now(tz_th).strftime("%Y-%m-%d %H:%M:%S")
    
    cards_html = ""
    for idx, insight in enumerate(insights_list):
        cards_html += f"""
        <div class='card'>
            <h3>💡 ข้อมูลคัดสรร #{idx+1}</h3>
            <p><strong>หัวข้อ:</strong> {insight.get('topic', 'N/A')}</p>
            <p>{insight.get('summary', 'ไม่มีข้อมูลสรุป')}</p>
            <p><small>📅 บันทึกเมื่อ: {insight.get('timestamp', 'N/A')}</small></p>
        </div>
        """
        
    if not cards_html:
        cards_html = "<p style='text-align:center; color:#888;'>ยังไม่มีข้อมูลคัดสรรในระบบขณะนี้</p>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Base44 Realtime AI Portal</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            header {{ text-align: center; margin-bottom: 30px; background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .card {{ background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 5px solid #1e3c72; }}
            footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #777; }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🚀 Base44 Centralized Switch Engine</h1>
                <p>ระบบควบคุม Multi-Agent อัจฉริยะสถานะ Live พร้อมทำงาน</p>
            </header>
            <main>
                {cards_html}
            </main>
            <footer>
                อัปเดตระบบเรียบร้อย (เวลาไทย): {update_time} | โหมดตรวจสอบสถานะหลังบ้านปราศจากข้อผิดพลาด
            </footer>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/")
async def root_portal():
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=generate_html_dashboard(), status_code=200)

# =====================================================================
# 📥 [Section 2] ระบบควบคุมคำสั่งแชทจากหน้าบ้าน Telegram Bot
# =====================================================================
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    welcome_text = (
        "🤖 **ยินดีต้อนรับเข้าสู่กองบัญชาการ Base44 Multi-Agent** 🚀\n\n"
        "ตอนนี้ระบบหลังบ้านเชื่อมต่อวงจรอย่างสมบูรณ์แบบแล้วครับพ้ม!\n"
        "นายท่านสามารถพิมพ์สั่งงานระบบการตลาด หรือทดสอบระบบได้ทันที"
    )
    await bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    print(f"💬 [Telegram Message Received]: {message.text}")
    # โยนงานเข้าตัวสลับสายงานแกนหลัก (Meta Orchestrator) ประมวลผลตรรกะ
    reply_content = meta_orchestrator.route_and_execute(message.text)
    await bot.reply_to(message, reply_content, parse_mode="Markdown")

# =====================================================================
# ⏰ [Section 3] Feature Expansion: ระบบตั้งเวลาออกล่าข้อมูลและแจ้งเตือนอัตโนมัติ
# =====================================================================
async def automated_hunting_loop():
    """
    ฟังก์ชันผู้พิทักษ์หลังบ้าน แอบทำงานเงียบๆ ทุกๆ ช่วงเวลาเพื่อส่งดีลเด็ดแจ้งเตือนนายท่าน
    """
    # ดึง Chat ID จริงที่บันทึกไว้ใน .env หากไม่มีจะล็อก Default ไว้คุยผ่านระบบบอทหลัก
    TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "5174095400") # หรือแก้เลข ID นายท่านใส่ตรงนี้ได้เลยครับ
    
    await asyncio.sleep(15) # ให้บอทสแตนด์บายระบบหลักให้พร้อม 15 วินาทีแรก
    print("🚀 [Automation System] ลูปตั้งเวลาสแกนข้อมูลเชิงรุก เริ่มทำงานเบื้องหลังแล้ว...")
    
    while True:
        try:
            print("🕒 [Automation System] ถึงรอบเวลาตรวจสอบ... สั่งการตลาดควบสายสืบออกทำงาน")
            
            # สั่งตัวแม่การตลาดไปดึงข้อมูลสายสืบและถอดรหัสวิเคราะห์แอดโฆษณา
            marketing_reports = growth_marketing_orchestrator.analyze_scraped_leads()
            
            for report in marketing_reports:
                # สั่งยิงกระสุนเตือนภัยเด้งเข้าแชทส่วนตัวของนายท่านโดยตรง!
                await bot.send_message(chat_id=TARGET_CHAT_ID, text=report, parse_mode="Markdown")
                await asyncio.sleep(2) # กันโดน Telegram บล็อกความถี่ (Rate Limit)
                
            print("✅ [Automation System] ส่งรายงานแจ้งเตือนเรียบร้อย เข้านอนรอสแกนรอบถัดไป")
            
            # ตั้งเวลาวนลูปซ้ำ: 3600 วินาที = 1 ชั่วโมง (ปรับเพิ่ม/ลดได้ตามใจชอบครับนายท่าน)
            await asyncio.sleep(3600)
            
        except Exception as e:
            print(f"⚠️ [Automation System Error] เกิดข้อผิดพลาดในลูปอัตโนมัติ: {e}")
            await asyncio.sleep(60)

# =====================================================================
# 🛫 [Section 4] ระบบผสานโครงสร้างสตาร์ทอัปคู่ขนาน (Uvicorn / FastAPI Startup)
# =====================================================================
@app.on_event("startup")
async def startup_event():
    print("⚡ [System Core Startup] เริ่มต้นโครงสร้างระบบนิเวศบอท...")
    
    # 1. ปลดล็อกระบบวนลูปแจ้งเตือนอัตโนมัติ (Background Task) ให้ทำงานขนานกันไป ไม่ขัดขาใคร
    asyncio.create_task(automated_hunting_loop())
    
    # 2. ปลดล็อก Webhook / Polling สั่งให้บอทเริ่มเงี่ยหูฟังคำสั่งคนพิมพ์แชท
    asyncio.create_task(bot.polling(non_stop=True, timeout=60))
    print("✅ [System Core Startup] สั่งเริ่มงาน Polling บอท และระบบ Automation เรียบร้อย!")