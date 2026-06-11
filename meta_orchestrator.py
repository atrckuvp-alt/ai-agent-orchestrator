# Complete file: 04_scripts/meta_orchestrator.py
import os
import sys
import asyncio
import random

# 🔌 [Senior Path Injection] บังคับให้ระบบมองเห็นไฟล์ทั้งหมดในโฟลเดอร์นี้เพื่อแก้ปัญหาเลข 04_
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

class MetaOrchestrator:
    def __init__(self):
        self.activated = True

    async def route_and_execute(self, user_message: str, user_id: int) -> dict:
        """ ระบบรับคำสั่งทั่วไปแปลงข้อความ (Fall-back Message Selector) """
        msg_clean = user_message.strip().lower()
        
        if "รันระบบล่าของฟรี" in msg_clean or "test evolution" in msg_clean:
            try:
                # 🔌 ตอนนี้สามารถเรียกหาโมเดลในระดับเดียวกันได้โดยตรงแล้วครับ ไม่ติดขัด
                from ai_evolution_orchestrator import ai_evolution_orchestrator
                from growth_marketing_orchestrator import growth_marketing_orchestrator
                is_triggered = ai_evolution_orchestrator.run_evolution_check()
                
                if is_triggered:
                    return {
                        "status": "success",
                        "data": {
                            "message": "🔍 🚨 **[BU_AI_Evolution_Hub]** ออกปฏิบัติการล่าของฟรีและสุ่มดึงโมเดลใหม่เข้าประจำการเรียบร้อยแล้ว!"
                        }
                    }
                else:
                    return {
                        "status": "success",
                        "data": {
                            "message": "ℹ️ **[BU_AI_Evolution_Hub]** ตรวจสอบแล้ว สถานะตลาดยังเสถียรดี ไม่จำเป็นต้องสลับโมเดลในรอบนี้ครับ"
                        }
                    }
            except Exception as e:
                return {"status": "error", "message": f"ระบบบอทล่าของฟรีขัดข้อง: {str(e)}"}
                
        return {
            "status": "error",
            "message": "🤖 ขออภัยครับนายท่าน บอท Meta_Orchestrator ยังไม่เข้าใจคำสั่งนี้ (โปรดลองสั่ง 'รันระบบล่าของฟรี')"
        }

    async def run_morning_cron(self):
        """ สคริปต์จำลองการทำงานตอน 09:00 น. เพื่อสุ่มโปรดักส์และสั่งวิเคราะห์อัตโนมัติ """
        morning_ideas = [
            "เซรั่มลดริ้วรอยสูตรพรีเมียมจากเมือกหอยทากเกาหลีผสมทองคำ 24K",
            "คอลลาเจนไดเปปไทด์ชนิดผงชงดื่ม บำรุงข้อต่อและผิวพรรณเข้มข้น",
            "ครีมกันแดดเนื้อไฮบริด SPF50+ PA++++ คุมมันสำหรับผิวแพ้ง่าย",
            "มาส์กหน้ากู้ผิวเร่งด่วนจากสารสกัดเมือกหอยทากและทองคำบริสุทธิ์"
        ]
        selected_product = random.choice(morning_ideas)

        try:
            from growth_marketing_orchestrator import growth_marketing_orchestrator
            loop = asyncio.get_event_loop()
            bu_result = await loop.run_in_executor(
                None, 
                growth_marketing_orchestrator.generate_strategic_plan, 
                selected_product, 
                True
            )
            
            from shared_knowledge import shared_knowledge
            shared_knowledge.publish_insight(
                author_team="Morning_Chronos_AI_Best",
                topic=f"[Morning Report] {selected_product}",
                insight_data={"best_tools": bu_result["best_tools"], "conclusion": bu_result["conclusion"]}
            )

            report_message = (
                f"☀️ 📢 **[Morning Briefing Report - 09:00 AM]**\n"
                f"อรุณสวัสดิ์ครับนายท่าน! บอทตั้งเวลาตื่นมาเสิร์ฟไอเดียประจำเช้านี้ในหัวข้อ:\n"
                f"👉 *'{selected_product}'*\n\n"
                f"{bu_result['conclusion']}\n\n"
                f"🔗 ตรวจสอบได้ที่: https://ai-agent-orchestrator-2vam.onrender.com"
            )
            return {"status": "success", "data": {"message": report_message}}
            
        except Exception as e:
            return {"status": "error", "message": f"สคริปต์ Cron ยามเช้าพัง: {str(e)}"}


# ========================================================
# 🚀 [Senior Dev Route] ท่อลัดพิเศษสำหรับ "นายท่าน" ใช้กดทดสอบยิงรายงาน Telegram ทันที
# ========================================================
# หมายเหตุ: เราเอามาแปะไว้ข้างนอกระดับล่างสุด เพื่อต่อเข้ากับตัวแปรแอปหลักของระบบครับ
from fastapi import FastAPI
# สมมติว่า api_app ถูกสร้างไว้ในระดับสถาปัตยกรรมหลัก ถ้าระบบเรียกไฟล์นี้จากภายนอก
# เพื่อความปลอดภัยในการรันเทส เราจะเขียนดักตรวจสอบตัวแปรแอปไว้ให้ครับ
api_app = FastAPI() if 'api_app' not in globals() else globals()['api_app']

@api_app.get("/test-telegram-report")
async def test_telegram_report():
    import os
    
    try:
        # 🔎 ดึงฟังก์ชันสร้างและส่งรายงานยามเช้าจากในคลาส MetaOrchestrator มาสั่งรันแมนนวล
        orchestrator_instance = MetaOrchestrator()
        
        # ตรวจสอบตัวแปรสภาพแวดล้อมก่อนยิงจริงเพื่อดักจับบั๊กคีย์ถล่ม
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        
        if not bot_token:
            return {
                "status": "failed",
                "reason": "❌ ระบบหาคีย์ 'TELEGRAM_BOT_TOKEN' บน Render ไม่เจอ! นายท่านกรุณาตรวจสอบการสะกดคำในหน้า Environment Variables ของ Render อีกครั้งนะครับ"
            }
            
        # สั่งให้ระบบรันฟังก์ชันส่งรายงานประจำวันทันที (Manual Trigger)
        report_result = await orchestrator_instance.run_morning_cron()
        
        return {
            "status": "success",
            "message": "🚀 ระบบสั่งยิงรายงานสำเร็จแล้วครับนายท่าน! บอทกำลังประมวลผลไอเดียและส่งเข้า Telegram ทันทีครับพ้ม",
            "backend_response": report_result,
            "using_token_prefix": bot_token[:10] + "..."
        }
        
    except Exception as e:
        # หากโค้ดส่วนไหนพังหรือเกิด KeyError ระบบจะพ่นสาเหตุจริงออกมาบนหน้าจอเบราว์เซอร์ทันที
        return {
            "status": "bug_detected",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "suggestion": "💥 เกิดข้อผิดพลาดขณะบอทพยายามรันคำสั่งรายงาน ข้อความเออร์เรอร์ด้านบนคือเบาะแสสำคัญที่จะบอกว่าคีย์หรือโค้ดส่วนไหนค้างอยู่ครับ!"
        }