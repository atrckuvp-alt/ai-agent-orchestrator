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
                            "message": "ℹ️ **[BU_AI_Evolution_Hub]** ตรวจสอบแล้ว สถานะตลาดยังเสถียรดี ไม่จำเป็นต้องสลับโมเดล in รอบนี้ครับ"
                        }
                    }
            except Exception as e:
                return {"status": "error", "message": f"ระบบบอทล่าของฟรีขัดข้อง: {str(e)}"}
                
        return {
            "status": "error",
            "message": "🤖 ขออภัยครับนายท่าน บอท Meta_Orchestrator ยังไม่เข้าใจคำสั่งนี้"
        }

    async def run_morning_cron(self):
        """ สคริปต์บอทรายงานยามเช้า 09:00 น. บังคับยิงข้อมูลเข้า Telegram """
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
            
            try:
                from shared_knowledge import shared_knowledge
                shared_knowledge.publish_insight(
                    author_team="Morning_Chronos_AI_Best",
                    topic=f"[Morning Report] {selected_product}",
                    insight_data={"best_tools": bu_result["best_tools"], "conclusion": bu_result["conclusion"]}
                )
            except Exception as e_share:
                print(f"⚠️ เตือน: อัปเดต shared_knowledge ขัดข้อง แต่ระบบจะรันส่งรายงานต่อ: {str(e_share)}")

            report_message = (
                f"☀️ 📢 **[Morning Briefing Report - 09:00 AM]**\n"
                f"อรุณสวัสดิ์ครับนายท่าน! บอทตั้งเวลาตื่นมาเสิร์ฟไอเดียประจำเช้านี้ในหัวข้อ:\n"
                f"👉 *'{selected_product}'*\n\n"
                f"{bu_result['conclusion']}\n\n"
                f"🔗 ตรวจสอบได้ที่: https://ai-agent-orchestrator-2vam.onrender.com"
            )
            return {"status": "success", "data": {"message": report_message}}
            
        except Exception as e:
            return {"status": "error", "message": f"สคริปต์ Cron ยามเช้าพังเนื่องจาก: {str(e)}"}

# 📦 สร้าง Instance เพื่อให้ไฟล์อื่น (เช่น telegram_bot.py) อิมพอร์ตไปใช้งานได้ทันที
meta_orchestrator = MetaOrchestrator()