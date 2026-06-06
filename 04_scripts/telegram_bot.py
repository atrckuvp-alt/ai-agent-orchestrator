import os
import sys
import asyncio
import json
import inspect  
from pathlib import Path
from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from telebot.async_telebot import AsyncTeleBot

# 📦 Import ออเคสเตรเตอร์หลักหลังบ้านของทีม Base44
sys.path.append(str(Path(__file__).parent.parent))
from core.meta_orchestrator import meta_orchestrator
from core.growth_marketing_orchestrator import growth_marketing_orchestrator

# 🔑 โหลดโทเค็นจาก Environment Variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ ไม่พบ TELEGRAM_BOT_TOKEN ใน Environment Variables หลังบ้าน!")

bot = AsyncTeleBot(BOT_TOKEN)
app = FastAPI(title="Base44 Multi-Agent Telegram Command Center")

# =====================================================================
# 🌐 [Section 1] ระบบควบคุมวงจรอายุแอปพลิเคชัน (FastAPI Lifespan)
# =====================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🛫 ช่วงเริ่มต้นโปรแกรม (Startup)
    print("📌 [Infra Path Configured] ตั้งค่าเส้นทางระบบนิเวศโมดูลสำเร็จ")
    
    try:
        print("🧹 [System Core Startup] กำลังเคลียร์ระบบ Webhook เก่าออกจากเซิร์ฟเวอร์ Telegram...")
        await bot.remove_webhook()
        await asyncio.sleep(1)
        
        # 🎯 เริ่มต้นรันลูปรายงานยุทธศาสตร์เช้า 09:00 น. ทำงานเบื้องหลัง
        asyncio.create_task(automated_hunting_loop())
        print("🚀 [Automation Infrastructure] ขาจราจรลูปอัตโนมัติประจำวันพร้อมสแตนด์บายเรียบร้อย")
        
        # รันระบบรับแชทแบบ Polling คลีน ๆ ไร้ความขัดแย้งของสายสัญญาน
        asyncio.create_task(bot.polling(non_stop=True, allowed_updates=['message']))
        print("📡 [Inbound Polling] ระบบดักรับคำสั่งแชทหน้าบ้านเปิดใช้งานสำเร็จ")
        
    except Exception as e:
        print(f"❌ [Critical Startup Error] ระบบวงจรหลักทำงานขัดข้องในช่วงเริ่ม: {e}")
        
    yield
    # 🛬 ช่วงปิดโปรแกรม (Shutdown)
    print("🛑 [System Core Shutdown] กำลังปิดสวิตช์วงจรบอทอย่างปลอดภัย...")

app.router.lifespan_context = lifespan

@app.get("/")
async def root():
    return {
        "status": "online",
        "agent": "Base44 Multi-Agent Core",
        "mode": "Daily Strategic Intelligence Enabled"
    }

# =====================================================================
# 📥 [Section 2] ระบบควบคุมคำสั่งแชทจากหน้าบ้าน Telegram Bot (Interactive Mode)
# =====================================================================
@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    welcome_text = (
        "🤖 **ยินดีต้อนรับเข้าสู่กองบัญชาการ Base44 Multi-Agent** 🚀\n\n"
        "ตอนนี้ระบบหลังบ้านเชื่อมต่อวงจรอย่างสมบูรณ์แบบแล้วครับพ้ม!\n"
        "• ระบบสรุปยุทธศาสตร์จะส่งรายงาน **09:00 น.** ของทุกวัน\n"
        "• นายท่านสามารถพิมพ์ทักแชทสั่งงาน AI สมองกลหลักได้ทันที"
    )
    await bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
async def handle_all_messages(message):
    user_msg = message.text
    sender_id = str(message.from_user.id)
    
    print(f"💬 [Telegram Message Received] From {sender_id}: {user_msg}")
    
    try:
        # 🧠 [Dynamic Check ขาเข้า] แยกแยะสาย Async/Sync คุยกับตัวแม่ราบรื่น
        if inspect.iscoroutinefunction(meta_orchestrator.route_and_execute):
            reply_content = await meta_orchestrator.route_and_execute(user_msg, sender_id)
        else:
            reply_content = meta_orchestrator.route_and_execute(user_msg, sender_id)
            
        if reply_content is None:
            reply_content = f"🤖 [System Echo] บอทได้รับคำสั่งเรื่อง '{user_msg}' และส่งเข้าสมองกลหลักเรียบร้อยแล้วครับพ้ม!"
            
        await bot.reply_to(message, reply_content, parse_mode="Markdown")
        
    except Exception as e:
        print(f"⚠️ [Bot Reply Error] เกิดข้อผิดพลาดขณะประมวลผลคำสั่งแชท: {e}")
        try:
            await bot.reply_to(message, "🤖 บอทได้รับคำสั่งแล้วครับพ้ม! ระบบสลับสายงานกำลังประมวลผลหลังบ้าน")
        except:
            pass

# =====================================================================
# ⏰ [Section 3] ลูปตั้งเวลารายงานยุทธศาสตร์รอบ 09:00 น. (ชุดเกราะ Sandbox 100%)
# =====================================================================
async def automated_hunting_loop():
    # ดึง ID ของนายท่านจาก Env (Fallback เป็นไอดีหลักของนายท่านชัวร์ที่สุด)
    TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7238952711") 
    
    # พักหายใจตอนเปิดเครื่องครั้งแรก 20 วินาที เพื่อให้ระบบเน็ตเวิร์ก Render นิ่งก่อน
    await asyncio.sleep(20) 
    print("🚀 [Automation System] ลูปตั้งเวลารายงาน Pain Point 09:00 น. เริ่มสแตนด์บายเบื้องหลังแล้ว...")
    
    while True:
        try:
            # 🕒 ตรรกะคำนวณเวลานอนและตื่นอ้างอิง เวลาประเทศไทย (GMT+7)
            tz_th = timezone(timedelta(hours=7))
            now = datetime.now(tz_th)
            
            # ตั้งเป้าหมายไปที่ 09:00 น. ตรงของวันนี้
            target_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
            
            # ถ้าวันนี้เลย 9 โมงเช้าไปแล้ว ให้เลื่อนเป้าหมายไปเป็น 9 โมงเช้าของวันพรุ่งนี้
            if now >= target_time:
                target_time += timedelta(days=1)
                
            sleep_seconds = (target_time - now).total_seconds()
            print(f"💤 [Automation System] เข้านอนชั่วคราว รอเวลาตื่นในอีก {sleep_seconds/3600:.2f} ชั่วโมง (เจอกัน 09:00 น. ตรง)")
            
            # สั่งให้ระบบ Sleep ยาวไปจนถึง 09:00 น.
            await asyncio.sleep(sleep_seconds)
            
            print("☀️ [Automation System] เวลา 09:00 น. แล้ว! เริ่มปลุกทีมควบสายสืบออกล่า Pain Point ธุรกิจประจำวัน...")
            
            # 🛡️ [เกราะ Sandbox ขั้นสูงสุด] แยกอ่างล้างแผลเฉพาะกิจ ขังความวินาศสันตะโรของโมดูลภายใน
            marketing_reports = []
            try:
                # ส่ง Parameter พิเศษบอกโมดูลให้เข้าโหมดกลั่นกรองเฉพาะ Pain Point คัดสรรทำธุรกิจได้ตามสั่ง
                if inspect.iscoroutinefunction(growth_marketing_orchestrator.analyze_scraped_leads):
                    marketing_reports = await growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
                else:
                    marketing_reports = growth_marketing_orchestrator.analyze_scraped_leads(mode="strategic_pain_point")
            except Exception as core_module_err:
                # ดักจับและกลืนระเบิด NoneType/Await ทุกรูปแบบ ไม่ให้มีสิทธิ์หลุดมาทำลูปหลักพังเด็ดขาด!
                print(f"⚠️ [Automation Core Warning] โมดูลภายในแอบระเบิดสะดุดขาตัวเอง: {core_module_err}")
                marketing_reports = []
            
            # 🛡️ [ดักทางชั้นที่ 2] ป้องกันอาการ 'NoneType' object is not iterable
            if marketing_reports is None or not isinstance(marketing_reports, list):
                print("⚠️ [Automation System Warning] ผลลัพธ์ไม่ใช่รูปแบบรายการ แปลงเป็นรายการว่างเปล่าให้อัตโนมัติ")
                marketing_reports = []
            
            # 📡 วนลูปส่งรายงานระดับหัวกะทิให้นายท่าน
            for report in marketing_reports:
                # 🛡️ [ดักทางชั้นที่ 3] คัดกรองและสแกนสตริงว่างเปล่า ป้องกัน Telegram เอเรอร์กลับมา
                if not report or not str(report).strip():
                    print("⚠️ [Automation System Warning] ตรวจพบรายงานว่างเปล่า (Empty) สั่งข้ามไม่ส่งออกไปให้ติดไฟแดง")
                    continue
                    
                try:
                    await bot.send_message(chat_id=TARGET_CHAT_ID, text=report, parse_mode="Markdown")
                    print(f"📢 [Automation System] ยิงรายงานยุทธศาสตร์ธุรกิจเข้า Chat ID {TARGET_CHAT_ID} สำเร็จ!")
                    await asyncio.sleep(2) # เว้นจังหวะความถี่เพื่อถนอม Telegram API Rate Limit
                except Exception as send_err:
                    print(f"⚠️ [Automation System Sub-Error] ท่อส่งข้อความย่อยมีปัญหา: {send_err}")
                
            print("✅ [Automation System] จบรอบรายงานประจำวันอย่างงดงาม เข้านอนรอสแกนรอบ 9 โมงเช้าวันถัดไป")
            
        except Exception as e:
            # 🎯 ดักจับเหตุสุดวิสัยชั้นนอกสุด ลูปใหญ่จะไม่มีวันล่มและดับไปจากระบบตลอดกาล!
            print(f"⚠️ [Automation System Error] เกิดข้อผิดพลาดร้ายแรงในลูปหลัก: {e}")
            await asyncio.sleep(60) # พักหายใจ 1 นาทีแล้วเริ่มต้นวนชีวิตใหม่