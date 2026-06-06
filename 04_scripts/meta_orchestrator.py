# Complete file: 04_scripts/meta_orchestrator.py
import asyncio
import random

class MetaOrchestrator:
    def __init__(self):
        self.activated = True

    async def route_and_execute(self, user_message: str, user_id: int) -> dict:
        """ ระบบรับคำสั่งทั่วไปแปลงข้อความ (Fall-back Message Selector) """
        # หากนายท่านพิมพ์คำสั่งขอดู Report ทั่วไป ให้แสดงแดชบอร์ดสรุป
        msg_clean = user_message.strip().lower()
        if "ขอดู report" in msg_clean or "report" in msg_clean:
            return {
                "status": "success",
                "data": {
                    "message": "📊 **[Base44 AI Command Center]**\n\nยินดีต้อนรับครับนายท่าน! ขณะนี้ระบบคิดสด Multi-Agent 4 ค่ายพร้อมใช้งานเต็มรูปแบบแล้ว\n\n💡 **วิธีการสั่งงานคิดสด:**\nพิมพ์คำว่า `ทำกลยุทธ์ [ตามด้วยสินค้า]` เช่น *'ทำกลยุทธ์ ครีมกันแดดสูตรน้ำ'* ระบบจะระดมสมองเจนแผนให้ทันทีครับ!\n\n🔗 หรือเปิดดูพอร์ตเทิลอัปเดตเรียลไทม์: https://ai-agent-orchestrator-2vam.onrender.com"
                }
            }
            
        return {
            "status": "success",
            "data": {
                "message": f"🤖 **[Meta Orchestrator]** ได้รับข้อความ '{user_message}' เรียบร้อยครับ\n\nหากต้องการให้ AI วิเคราะห์แผนธุรกิจ ดร.แสงสุข กรุณาพิมพ์ขึ้นต้นด้วยคำว่า **'ทำกลยุทธ์ ...'** ได้เลยครับพ้ม!"
            }
        }

    async def execute_scheduled_task(self, user_id: int) -> dict:
        """ ⏰ [สมองกลางตั้งเวลา 9 โมงเช้า] สั่งการให้ AI 4 ค่ายแอบประมวลผลสรุปเนื้อหาอัจฉริยะส่งตรงหานายท่าน """
        print("⏰ [Meta Orchestrator] เริ่มขบวนการผลิตรายงาน 9 โมงเช้าผ่านขุมพลัง AI คิดสด...")
        
        # คลังสินค้าต้นแบบสำหรับสุ่มส่งรายงานให้นายท่านตรวจไอเดียทุกเช้าแบบไม่ซ้ำจำเจ
        morning_ideas = [
            "อาหารเสริมสกัดพรีเมียมจากถั่งเช่าและโสมสกัดสำหรับผู้บริหารยุคใหม่",
            "ยาสระผมสมุนไพรสูตรลดการหลุดร่วงของเส้นผมชะลอวัย",
            "กาแฟออร์แกนิกคั่วบดดริปสดผสมสารสกัดบำรุงสมอง",
            "ครีมบำรุงผิวหน้าออร์แกนิกจากสารสกัดเมือกหอยทากและทองคำบริสุทธิ์"
        ]
        selected_product = random.choice(morning_ideas)

        try:
            # ดึงผู้จัดการยูนิตการตลาดเข้ามาสั่งงานคิดสดข้ามค่ายทันที
            from growth_marketing_orchestrator import growth_marketing_orchestrator
            
            # รันการคิดวิเคราะห์กลยุทธ์และการสร้างเนื้อหาจาก AI จริงแบบหลังบ้าน
            loop = asyncio.get_event_loop()
            bu_result = await loop.run_in_executor(
                None, 
                growth_marketing_orchestrator.generate_strategic_plan, 
                selected_product, 
                True  # รันในโหมด Daily Job
            )
            
            # บันทึกเข้าแชร์คลังความรู้ส่วนกลาง ดันขึ้นหน้าเว็บ Portal
            from shared_knowledge import shared_knowledge
            shared_knowledge.publish_insight(
                author_team="Morning_Chronos_AI_Best",
                topic=f"[Morning Report] {selected_product}",
                insight_data={"best_tools": bu_result["best_tools"], "conclusion": bu_result["conclusion"]}
            )

            report_message = (
                f"☀️ 📢 **[Morning Briefing Report - 09:00 AM]**\n"
                f"อรุณสวัสดิ์ครับนายท่าน! บอทตั้งเวลาตื่นมาเสิร์ฟไอเดียทำเงินประจำเช้านี้ในหัวข้อ:\n"
                f"👉 *'{selected_product}'*\n\n"
                f"{bu_result['conclusion']}\n\n"
                f"🔗 แผนงานนี้ถูกอัปโหลดขึ้นหน้าเว็บหลักเรียบร้อยแล้ว ตรวจสอบได้ที่: https://ai-agent-orchestrator-2vam.onrender.com"
            )
            
            return {
                "status": "success",
                "data": {
                    "message": report_message
                }
            }

        except Exception as e:
            print(f"⚠️ [Scheduled Task Error] ไหลลื่นติดขัด: {e}")
            return {
                "status": "error",
                "data": {
                    "message": f"☀️ ⏰ **[Morning Briefing]** เกิดข้อผิดพลาดในการดึงสมองกลด่วน: {e}"
                }
            }

meta_orchestrator = MetaOrchestrator()