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
                            "message": "🔍 🚨 **[BU_AI_Evolution_Hub]** ออกปฏิบัติการคัดกรองโมเดลเสร็จสิ้น!\n\n🤖 ตรวจพบโมเดลฟรีตัวใหม่ที่ผ่านเกณฑ์กฎเหล็ก และได้ส่ง **'การ์ดคำขออนุมัติสีแดง'** ขึ้นไปลอยเด่นบนหน้าเว็บ Base44 Portal เรียบร้อยแล้วครับนายท่าน! ไปเปิดตรวจดูได้เลยครับพ้ม!"
                        }
                    }
                else:
                    return {
                        "status": "success",
                        "data": {
                            "message": "🔍 **[BU_AI_Evolution_Hub]** ออกปฏิบัติการแล้ว แต่โมเดลใหม่ๆ ในตลาดยังทดสอบ Sandbox ไม่ผ่านเกณฑ์กฎเหล็กในรอบนี้ครับ!"
                        }
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "data": {
                        "message": f"⚠️ เกิดข้อผิดพลาดในระบบล่าของฟรี: {e}"
                    }
                }

        if "ขอดู report" in msg_clean or "report" in msg_clean:
            return {
                "status": "success",
                "data": {
                    "message": "📊 **[Base44 AI Command Center]**\n\nยินดีต้อนรับครับนายท่าน! ขณะนี้ระบบคิดสด Multi-Agent พร้อมใช้งานเต็มรูปแบบแล้ว\n\n💡 **วิธีการสั่งงานคิดสด:**\nพิมพ์คำว่า `ทำกลยุทธ์ [ตามด้วยสินค้า]` เช่น *'ทำกลยุทธ์ ครีมกันแดดสูตรน้ำ'*\n\n🛠️ **คำสั่งทดสอบระบบสายล่าของฟรี:**\nพิมพ์คำว่า `รันระบบล่าของฟรี` เพื่อสั่งให้บอทคัดกรองโมเดลใหม่ขึ้นหน้าเว็บ\n\n🔗 เปิดดูพอร์ตเทิลเว็บ: https://ai-agent-orchestrator-2vam.onrender.com"
                }
            }
            
        return {
            "status": "success",
            "data": {
                "message": f"🤖 **[Meta Orchestrator]** ได้รับข้อความ '{user_message}' เรียบร้อยครับ\n\nหากต้องการให้ AI วิเคราะห์แผนธุรกิจ ดร.แสงสุข กรุณาพิมพ์ขึ้นต้นด้วยคำว่า **'ทำกลยุทธ์ ...'** ได้เลยครับพ้ม!"
            }
        }

    async def execute_scheduled_task(self, user_id: int) -> dict:
        """ ⏰ [สมองกลางตั้งเวลา 9 โมงเช้า] สั่งการให้ AI 4 ค่ายสรุปเนื้อหาส่งตรงหานายท่าน """
        print("⏰ [Meta Orchestrator] เริ่มขบวนการผลิตรายงาน 9 โมงเช้าผ่านขุมพลัง AI คิดสด...")
        morning_ideas = [
            "อาหารเสริมสกัดพรีเมียมจากถั่งเช่าและโสมสกัดสำหรับผู้บริหารยุคใหม่",
            "ยาสระผมสมุนไพรสูตรลดการหลุดร่วงของเส้นผมชะลอวัย",
            "กาแฟออร์แกนิกคั่วบดดริปสดผสมสารสกัดบำรุงสมอง",
            "ครีมบำรุงผิวหน้าออร์แกนิกจากสารสกัดเมือกหอยทากและทองคำบริสุทธิ์"
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
            return {"status": "error", "data": {"message": f"☀️ ⏰ **[Morning Briefing]** ข้อผิดพลาด: {e}"}}

meta_orchestrator = MetaOrchestrator()