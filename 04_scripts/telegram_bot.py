import os
import sys
import asyncio
import json
import inspect
from pathlib import Path
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

# 📂 [Infra] แก้ไข Path ให้ชี้ไปที่ Root ของโปรเจกต์โดยตรง
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ตอนนี้ Import จาก core จะแม่นยำ 100% เพราะเราเพิ่ม PROJECT_ROOT เข้าไปใน sys.path แล้ว
from core.meta_orchestrator import meta_orchestrator
from core.growth_marketing_orchestrator import growth_marketing_orchestrator

from fastapi import FastAPI
from telebot.async_telebot import AsyncTeleBot

# 🔑 โหลดโทเค็น
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(BOT_TOKEN) if BOT_TOKEN else None
app = FastAPI(title="Base44 Multi-Agent Telegram Command Center")

# =====================================================================
# 🌐 [Section 1] ระบบควบคุมวงจรอายุแอปพลิเคชัน
# =====================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"📌 [Infra] Project Root: {PROJECT_ROOT}")
    if bot:
        await bot.remove_webhook()
        asyncio.create_task(bot.polling(non_stop=True, allowed_updates=['message']))
        asyncio.create_task(automated_hunting_loop())
    yield

app.router.lifespan_context = lifespan

# =====================================================================
# ⏰ [Section 2] ลูปตั้งเวลารายงานยุทธศาสตร์รอบ 09:00 น.
# =====================================================================
async def automated_hunting_loop():
    TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7238952711")
    await asyncio.sleep(20)
    while True:
        try:
            tz_th = timezone(timedelta(hours=7))
            now = datetime.now(tz_th)
            target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
            if now >= target_time:
                target_time += timedelta(days=1)
            
            await asyncio.sleep((target_time - now).total_seconds())
            
            marketing_reports = []
            try:
                if inspect.iscoroutinefunction(growth_marketing_orchestrator.analyze_scraped_leads):
                    marketing_reports = await growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
                else:
                    marketing_reports = growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
            except Exception as e:
                print(f"⚠️ [Core Warning] {e}")
            
            if isinstance(marketing_reports, list):
                for report in marketing_reports:
                    if report and str(report).strip():
                        await bot.send_message(chat_id=TARGET_CHAT_ID, text=report, parse_mode="Markdown")
                        await asyncio.sleep(2)
        except Exception as e:
            print(f"⚠️ [Loop Error] {e}")
            await asyncio.sleep(60)

# =====================================================================
# 📥 [Section 3] คำสั่งแชทหน้าบ้าน
# =====================================================================
@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    try:
        reply = await meta_orchestrator.route_and_execute(message.text, str(message.from_user.id))
        await bot.reply_to(message, reply or "🤖 บอททำงานเรียบร้อยครับ")
    except Exception as e:
        print(f"⚠️ [Chat Error] {e}")

# =====================================================================
# 🏁 [Section 4] รันตัวเองด้วย Uvicorn (Self-Executable)
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("telegram_bot:app", host="0.0.0.0", port=port, reload=False)