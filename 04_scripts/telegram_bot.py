# 🚨 สำคัญที่สุด: ต้องเพิ่ม Path ก่อน import ทุกอย่าง
import sys
from pathlib import Path

# ปักหมุด Root Directory ของโปรเจกต์
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ตอนนี้ Import จาก core จะทำงานได้แน่นอน
import os
import asyncio
import json
import inspect
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

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
                # 🛡️ Sandbox 
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
# 🏁 [Section 3] รันตัวเอง
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    # ระบุให้ชัดเจนว่า app อยู่ในโมดูลไหน
    uvicorn.run("04_scripts.telegram_bot:app", host="0.0.0.0", port=port, reload=False)