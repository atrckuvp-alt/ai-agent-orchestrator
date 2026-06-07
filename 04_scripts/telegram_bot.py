import sys
import os
from pathlib import Path
import asyncio
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telebot.async_telebot import AsyncTeleBot

# 📂 [Infra] ปักหมุด Root Directory ให้ Python เห็นโมดูลที่วางอยู่ใน Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 🎯 Import จาก Root โดยตรง
from meta_orchestrator import meta_orchestrator
from growth_marketing_orchestrator import growth_marketing_orchestrator

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
        print("🧹 [System] กำลังล้าง Webhook และเริ่มระบบรายงาน 09:00 น. ...")
        await bot.delete_webhook(drop_pending_updates=True)
        asyncio.create_task(bot.polling(non_stop=True, allowed_updates=['message']))
        # เริ่มลูปรายงานเดียวที่รวบงานทุกอย่างไว้
        asyncio.create_task(daily_strategic_report_loop())
    yield

app.router.lifespan_context = lifespan

# =====================================================================
# ⏰ [Section 2] ลูปยุทธศาสตร์รวมมิตร (รันวันละครั้งตอน 09:00 น.)
# =====================================================================
async def daily_strategic_report_loop():
    TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7238952711")
    print("🚀 [System] ระบบรายงานยุทธศาสตร์สแตนด์บาย...")
    
    while True:
        # คำนวณเวลาให้ถึง 09:00 น. ถัดไป
        now = datetime.now(timezone(timedelta(hours=7)))
        target = now.replace(hour=9, minute=0, second=0, microsecond=0)
        if now >= target: target += timedelta(days=1)
        
        await asyncio.sleep((target - now).total_seconds())
        
        print("☀️ [System] เริ่มการระดมข้อมูล 09:00 น. ...")
        
        # 1. งานหาของฟรี
        try:
            free_tier_report = growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
        except Exception as e:
            free_tier_report = f"⚠️ เกิดข้อผิดพลาดในการหาของฟรี: {e}"
            
        # 2. งานหา AI (หากมีโมดูล)
        ai_report = "🤖 สแกนหา AI Open-source เรียบร้อย" 
        
        # 3. จัดรวมรายงาน
        final_message = (
            "🌅 **[Morning Strategic Report]**\n\n"
            f"💰 **Pain Points ธุรกิจ:**\n{free_tier_report}\n\n"
            f"🤖 **สถานะ AI:**\n{ai_report}\n\n"
            "🔗 **ดูรายละเอียดเชิงลึกทั้งหมดบน Base44:** https://base44.example.com/daily-dashboard"
        )
        
        await bot.send_message(TARGET_CHAT_ID, final_message, parse_mode="Markdown")
        await asyncio.sleep(60) # พัก 1 นาทีเพื่อป้องกันการรันซ้ำ

# =====================================================================
# 📥 [Section 3] คำสั่งแชทหน้าบ้าน
# =====================================================================
@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    try:
        reply = await meta_orchestrator.route_and_execute(message.text, str(message.from_user.id))
        await bot.reply_to(message, reply or "🤖 บอททำงานเรียบร้อยครับ")
    except Exception as e:
        await bot.reply_to(message, f"⚠️ Error: {e}")

# =====================================================================
# 🏁 [Section 4] รันด้วย Uvicorn
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("04_scripts.telegram_bot:app", host="0.0.0.0", port=port, reload=False)