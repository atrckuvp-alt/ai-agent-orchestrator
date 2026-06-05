# Complete file: 04_scripts/telegram_bot.py
import os
import sys
import asyncio
import datetime
import json
from pathlib import Path
from telebot.types import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
KNOWLEDGE_BASE_PATH = ROOT / "00_memory" / "shared_knowledge_base.json"

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

load_dotenv(dotenv_path=ROOT / ".env")
from meta_orchestrator import meta_orchestrator
from growth_marketing_orchestrator import growth_marketing_orchestrator

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("💥 ไม่พบ TELEGRAM_BOT_TOKEN ในระบบ Environment Variables!")

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)

# =====================================================================
# 🌐 [WEB PORTAL ENGINE - HTML DASHBOARD GENERATOR FOR MASTER]
# =====================================================================
def generate_html_dashboard():
    try:
        if KNOWLEDGE_BASE_PATH.exists():
            db = json.loads(KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8"))
        else:
            db = {"insights": []}
    except Exception:
        db = {"insights": []}

    insights_list = db.get("insights", [])
    tz_th = datetime.timezone(datetime.timedelta(hours=7))
    update_time = datetime.datetime.now(tz_th).strftime("%Y-%m-%d %H:%M:%S")

    cards_html = ""
    if not insights_list:
        cards_html = """
        <div style="text-align: center; padding: 40px; color: #8898aa; background: #1e293b; border-radius: 12px; border: 1px dashed #334155;">
            📬 ยินดีต้อนรับครับนายท่าน! ขณะนี้ยังไม่มีแผนงานปั๊มเงินที่ได้รับการอนุมัติอัปเดตลงระบบ
        </div>
        """
    else:
        for idx, item in enumerate(reversed(insights_list), 1):
            tools_badges = "".join([f'<span style="background: #2563eb; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem; margin-right: 6px; display: inline-block;">🛠️ {t.get("name","Tool")}</span>' for t in item.get("tools", [])])
            cards_html += f"""
            <div style="background: #1e293b; border: 1px solid #334155; padding: 24px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #334155; padding-bottom: 12px;">
                    <span style="color: #38bdf8; font-weight: bold; font-size: 1.1rem;">🔥 แผนงานทำเงินที่ #{len(insights_list) - idx + 1}</span>
                    <span style="background: #0f172a; color: #34d399; padding: 4px 12px; border-radius: 6px; font-size: 0.85rem; font-family: monospace;">⚙️ {item.get('author_team','Unknown BU')}</span>
                </div>
                <div style="margin-bottom: 12px;">
                    <strong style="color: #94a3b8; display: block; margin-bottom: 4px;">🔍 โจทย์วิจัย:</strong>
                    <span style="color: #f8fafc; font-size: 1.05rem;">{item.get('topic','N/A')}</span>
                </div>
                <div style="margin-bottom: 16px;">
                    <strong style="color: #94a3b8; display: block; margin-bottom: 4px;">📝 บทสรุปแผนยุทธศาสตร์ความสำเร็จ:</strong>
                    <div style="color: #e2e8f0; line-height: 1.6; margin: 0; background: #0f172a; padding: 14px; border-radius: 8px; white-space: pre-wrap;">{item.get('conclusion','-')}</div>
                </div>
                <div>
                    <strong style="color: #94a3b8; display: block; margin-bottom: 6px;">🎯 เครื่องมือปั๊มเงินคัดสรรพิเศษ (Base44 Automated Dynamic):</strong>
                    {tools_badges if tools_badges else '<span style="color: #64748b;">ไม่มีการใช้เครื่องมือพิเศษ</span>'}
                </div>
            </div>
            """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Base44 Command Center Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #1e3a8a, #0f172a); border: 1px solid #2563eb; padding: 30px; border-radius: 16px; margin-bottom: 24px; text-align: center; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0 0 10px 0; color: #38bdf8; font-size: 2rem;">🌐 Base44 Command Center Portal</h1>
                <p style="margin: 0; color: #94a3b8;">ระบบรายงานผลลัพธ์ข้อมูลแผนงานปั๊มเงินและไอเดียธุรกิจดิจิทัลของนายท่าน</p>
                <div style="margin-top: 15px; font-size: 0.85rem; color: #34d399; background: #0f172a; display: inline-block; padding: 6px 14px; border-radius: 30px;">
                    🟢 สถานะระบบหลังบ้าน: Live & Connected | 🕒 อัปเดตล่าสุด: {update_time} น.
                </div>
            </div>
            <h2 style="color: #f1f5f9; border-left: 4px solid #38bdf8; padding-left: 10px; margin-bottom: 16px; font-size: 1.3rem;">📋 รายการข้อมูลความรู้ยุทธศาสตร์ปั๊มเงิน (Approved)</h2>
            {cards_html}
        </div>
    </body>
    </html>
    """
    return full_html

# =====================================================================
# 🌐 [WEBHOOK ENGINE - ASGI APP FOR RENDER]
# =====================================================================
async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                MY_USER_ID = 7238952711
                asyncio.create_task(autonomous_cron_loop(bot, MY_USER_ID))
                print("📡 [Webhook Active] ระบบสมองกลและหน้าเว็บ Portal เปิดทำงานแล้ว...")
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await send({'type': 'lifespan.shutdown.complete'})
                return
                
    elif scope['type'] == 'http' and scope['path'] == '/webhook' and scope['method'] == 'POST':
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)
            
        if body:
            try:
                json_string = body.decode('utf-8')
                update_dict = json.loads(json_string)
                if "message" in update_dict:
                    msg_obj = update_dict["message"]
                    chat_id = msg_obj["chat"]["id"]
                    user_id = msg_obj["from"]["id"]
                    user_text = msg_obj.get("text", "")
                    
                    # 💡 คีย์เวิร์ดพิเศษสำหรับสั่งสุ่ม Content รายวัน
                    if user_text.strip().lower() == "run daily content":
                        print("⏰ [Chronos Active Trigger] นายท่านสั่งรันระบบ Content รายวันอัตโนมัติ!")
                        bu_result = growth_marketing_orchestrator.generate_strategic_plan("ธุรกิจข้าวสารสุขภาพรายวัน", is_daily_job=True)
                        
                        from shared_knowledge import shared_knowledge
                        shared_knowledge.publish_insight(
                            author_team="growth_marketing_bu_daily",
                            topic="ระบบสุ่มผลิตเนื้อหารายวันอัตโนมัติ (Automation)",
                            insight_data={"best_tools": bu_result["best_tools"], "conclusion": bu_result["conclusion"]}
                        )
                        
                        await bot.send_message(
                            chat_id=chat_id, 
                            text=f"⏰ **[Daily Automation Success]**\nโรงงานสมองกลได้สุ่มสร้างเนื้อหาประจำวัน และดันขึ้นหน้าเว็บ **Base44 Portal** ให้เรียบร้อยแล้วโดยไม่ต้องรออนุมัติครับพ้ม!\n\n🔗 คลิกเปิดดูหน้าเว็บ: https://ai-agent-orchestrator-2vam.onrender.com",
                            parse_mode="Markdown"
                        )
                    # 💡 ตรวจจับคีย์เวิร์ดพิเศษสำหรับสั่งทดสอบคู่ขนานหลายสินค้าพร้อมกัน
                    elif user_text.strip().lower() == "run parallel test":
                        print("🏎️ [Parallel Engine Active] เริ่มทำการประมวลผลกลยุทธ์ 2 โปรดักก์พร้อมกันขนานกัน!")
                        
                        # รันสินค้าชิ้นที่ 1 และ 2 คู่ขนานพร้อมกันแบบ Asynchronous ทันที
                        loop = asyncio.get_event_loop()
                        task1 = loop.run_in_executor(None, growth_marketing_orchestrator.generate_strategic_plan, "ข้าวสารปลอดสารพิษดัชนีน้ำตาลต่ำ", True)
                        task2 = loop.run_in_executor(None, growth_marketing_orchestrator.generate_strategic_plan, "แชมพูสมุนไพรออร์แกนิกสกัดเย็นลดผมร่วง", True)
                        
                        res1, res2 = await asyncio.gather(task1, task2)
                        
                        from shared_knowledge import shared_knowledge
                        shared_knowledge.publish_insight(author_team="bu_parallel_1", topic="[Parallel] ธุรกิจข้าวสารสุขภาพ", insight_data={"best_tools": res1["best_tools"], "conclusion": res1["conclusion"]})
                        shared_knowledge.publish_insight(author_team="bu_parallel_2", topic="[Parallel] ธุรกิจแชมพูออร์แกนิก", insight_data={"best_tools": res2["best_tools"], "conclusion": res2["conclusion"]})
                        
                        await bot.send_message(
                            chat_id=chat_id, 
                            text=f"🏎️ **[Parallel Processing Complete]**\nระบบได้ทำการวิเคราะห์แผนงานของทั้ง **'ข้าวสาร'** และ **'แชมพูสมุนไพร'** พร้อมกันแบบคู่ขนานข้ามอุตสาหกรรมเรียบร้อยแล้ว! ข้อมูลไหลแยกการ์ดกันอย่างอิสระบนหน้าเว็บ\n\n🔗 คลิกเปิดพอร์ตเทิลดูผลลัพธ์คู่ขนาน: https://ai-agent-orchestrator-2vam.onrender.com",
                            parse_mode="Markdown"
                        )
                    else:
                        print(f"📥 [Direct Message Trigger] จาก {user_id}: {user_text}")
                        orchestrator_response = await meta_orchestrator.route_and_execute(user_message=user_text, user_id=user_id)
                        
                        if orchestrator_response and "data" in orchestrator_response:
                            data_payload = orchestrator_response["data"]
                            if "message" in data_payload:
                                reply_markup = None
                                if "inline_buttons" in data_payload:
                                    markup = InlineKeyboardMarkup()
                                    for btn in data_payload["inline_buttons"]:
                                        markup.add(InlineKeyboardButton(text=btn["text"], url=btn["url"]))
                                    reply_markup = markup
                                    
                                await bot.send_message(chat_id=chat_id, text=data_payload["message"], reply_markup=reply_markup, parse_mode="Markdown")
                else:
                    update = Update.de_json(json_string)
                    await bot.process_new_updates([update])
            except Exception as e:
                print(f"⚠️ [Webhook Parse Error] ถอดรหัสพลาด: {e}")
                
        await send({'type': 'http.response.start', 'status': 200, 'headers': [[b'content-type', b'text/plain']]})
        await send({'type': 'http.response.body', 'body': b'OK'})
        
    else:
        html_content = generate_html_dashboard().encode('utf-8')
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [[b'content-type', b'text/html; charset=utf-8']],
        })
        await send({'type': 'http.response.body', 'body': html_content})

# =====================================================================
# ⏰ [⏰ CHRONOS WATCHER - TIMEZONE FIXED]
# =====================================================================
async def autonomous_cron_loop(bot_instance, target_user_id: int):
    print("⏳ [Chronos Watcher] ระบบเฝ้าระวังเวลารายงานเช้า เปิดทำงานคู่ขนาน...")
    has_run_today = False
    while True:
        try:
            tz_thailand = datetime.timezone(datetime.timedelta(hours=7))
            now = datetime.datetime.now(tz_thailand)
            if now.hour == 9 and now.minute == 0:
                if not has_run_today:
                    await bot_instance.send_message(chat_id=target_user_id, text="⏰ **[Morning Briefing]** ระบบเริ่มประมวลผลรายงานยุทธศาสตร์ประจำวันแล้วครับ...")
                    scheduled_result = await meta_orchestrator.execute_scheduled_task(user_id=target_user_id)
                    if scheduled_result and "data" in scheduled_result and "message" in scheduled_result["data"]:
                        await bot_instance.send_message(chat_id=target_user_id, text=scheduled_result["data"]["message"])
                    has_run_today = True
            else:
                if now.hour != 9 or now.minute != 0:
                    has_run_today = False
            await asyncio.sleep(20)
        except Exception as cron_err:
            print(f"⚠️ [Chronos Warning] ลูปเวลาติดขัด: {cron_err}")
            await asyncio.sleep(30)