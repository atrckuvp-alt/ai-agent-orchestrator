import sys
import os
from pathlib import Path
import asyncio
import inspect
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, Request
from telebot.async_telebot import AsyncTeleBot
import telebot

# 📂 [Infra] ปักหมุด Root Directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 🎯 Import จาก Root โดยตรง
from meta_orchestrator import meta_orchestrator
from growth_marketing_orchestrator import growth_marketing_orchestrator

# 🔑 โหลดโทเค็นและตั้งค่า Webhook
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL") 
WEBHOOK_URL = f"{RENDER_URL}/{BOT_TOKEN}" if RENDER_URL else None

bot = AsyncTeleBot(BOT_TOKEN) if BOT_TOKEN else None
app = FastAPI(title="Base44 Multi-Agent Telegram Command Center")

# =====================================================================
# 🚨 [New Section] ประตูหน้าบ้านสำหรับปลุก UptimeRobot (Health Check)
# =====================================================================
@app.get("/")
async def health_check():
    # เมื่อ UptimeRobot ยิงมาที่นี่ จะได้ 200 OK ทันที ระบบจะเปลี่ยนเป็นสีเขียว (Up)
    return {
        "status": "healthy", 
        "message": "Base44 Command Center is Live!",
        "timestamp": datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S")
    }

# =====================================================================
# ⏰ [Section 1] ลูปยุทธศาสตร์รวมมิตร (รันวันละครั้งตอน 09:00 น.)
# =====================================================================
async def daily_strategic_report_loop():
    TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7238952711")
    print("🚀 [System] ระบบรายงานยุทธศาสตร์ 09:00 น. เริ่มสแตนด์บาย...")
    
    while True:
        try:
            tz_th = timezone(timedelta(hours=7))
            now = datetime.now(tz_th)
            target = now.replace(hour=9, minute=0, second=0, microsecond=0)
            if now >= target: 
                target += timedelta(days=1)
            
            seconds_to_wait = (target - now).total_seconds()
            print(f"⏰ [System] กำลังรออีก {seconds_to_wait} วินาที...")
            await asyncio.sleep(seconds_to_wait)
            
            print("☀️ [System] เริ่มการระดมข้อมูล 09:00 น. ...")
            
            # 1. งานหาของฟรี
            marketing_reports = []
            try:
                if inspect.iscoroutinefunction(growth_marketing_orchestrator.analyze_scraped_leads):
                    marketing_reports = await growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
                else:
                    marketing_reports = growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
            except Exception as e:
                marketing_reports = [f"⚠️ เกิดข้อผิดพลาดในการหาของฟรี: {e}"]
            
            free_tier_report = ""
            if isinstance(marketing_reports, list):
                free_tier_report = "\n".join([str(r) for r in marketing_reports if r])
            else:
                free_tier_report = str(marketing_reports)
            
            # 2. งานหา AI Open-source Free-tier (ล็อกโครงร่างไว้ลุยงานชุด B)
            ai_report = "🤖 บอทสแกน AI Open-source สแตนด์บาย (พร้อมเชื่อมโยง Core ชุด B)"
            
            # 3. จัดรวมรายงานพร้อม Link Base44
            final_message = (
                "🌅 **[Morning Strategic Report]**\n\n"
                f"💰 **Pain Points ธุรกิจ & แหล่งฟรี:**\n{free_tier_report}\n\n"
                f"🤖 **ข้อมูล AI Open-source ล่าสุด:**\n{ai_report}\n\n"
                "🔗 **ดูรายละเอียดเชิงลึกทั้งหมดบนหน้าเว็บ Base44:**\nhttps://base44.pro/dashboard"
            )
            
            if bot:
                await bot.send_message(chat_id=TARGET_CHAT_ID, text=final_message, parse_mode="Markdown")
                print("✅ [System] ส่งรายงานยุทธศาสตร์เรียบร้อยแล้ว!")
            
            await asyncio.sleep(60) 
        except Exception as e:
            print(f"⚠️ [Loop Error] {e}")
            await asyncio.sleep(60)

# =====================================================================
# 🌐 [Section 2] ระบบควบคุม Webhook
# =====================================================================
@app.on_event("startup")
async def on_startup():
    asyncio.create_task(daily_strategic_report_loop())
    
    if bot and WEBHOOK_URL:
        print(f"🧹 [System] กำลังสลับไปใช้ระบบ Webhook ที่ URL: {WEBHOOK_URL}")
        await bot.remove_webhook()
        await bot.set_webhook(url=WEBHOOK_URL)
        print("✅ [System] เปลี่ยนไปใช้ระบบ Webhook สำเร็จ บอทพร้อมรบ!")
    elif bot:
        print("⚠️ [System] ไม่พบ URL ของ Render, สลับกลับไปใช้ระบบ Polling สำรอง...")
        await bot.remove_webhook()
        asyncio.create_task(bot.polling(non_stop=True, allowed_updates=['message']))

if WEBHOOK_URL:
    @app.post(f"/{BOT_TOKEN}")
    async def process_webhook(request: Request):
        try:
            json_str = await request.json()
            update = telebot.types.Update.de_json(json_str)
            await bot.process_new_updates([update])
        except Exception as e:
            print(f"⚠️ [Webhook Error] {e}")
        return {"status": "ok"}

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("04_scripts.telegram_bot:app", host="0.0.0.0", port=port, reload=False)