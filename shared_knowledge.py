# Complete file: 04_scripts/shared_knowledge.py
import datetime

class SharedKnowledge:
    def __init__(self):
        # คลังจัดเก็บข้อมูล Insight ชั่วคราวบน Memory ของเซิร์ฟเวอร์
        self.insights_db = []
        print("🗄️ [Shared Knowledge System] คลังความรู้ส่วนกลางพร้อมสแตนบายบน Memory")

    def publish_insight(self, author_team: str, topic: str, insight_data: dict) -> bool:
        """ ฟังก์ชันหลักในการบันทึกข้อมูล Insight และดันขึ้นสู่ระบบหน้าเว็บ Portal """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            record = {
                "id": len(self.insights_db) + 1,
                "timestamp": timestamp,
                "author": author_team,
                "topic": topic,
                "best_tools": insight_data.get("best_tools", []),
                "conclusion": insight_data.get("conclusion", "ไม่มีข้อมูลสรุป")
            }
            
            # บันทึกลงฐานข้อมูลชั่วคราว
            self.insights_db.insert(0, record)  # เอาข้อมูลใหม่ขึ้นก่อนเสมอ
            print(f"✅ [Shared Knowledge] บันทึกข้อมูลสำเร็จจากทีม: '{author_team}' ในหัวข้อ '{topic}'")
            return True
        except Exception as e:
            print(f"⚠️ [Shared Knowledge Error] ไม่สามารถบันทึกข้อมูลได้: {e}")
            return False

    def request_ai_upgrade(self, upgrade_data: dict) -> bool:
        """ 🚨 [ฟังก์ชันใหม่] ส่งคำร้องขออนุมัติเปลี่ยนโมเดลฟรีตัวใหม่ขึ้นหน้า Base44 Portal """
        insight_content = (
            f"🚨 **[AI UPGRADE REQUEST]** ตรวจพบโมเดลใหม่ที่ดีกว่าและตรงตามกฎเหล็ก!\n\n"
            f"• **โมเดลที่แนะนำให้ใช้:** `{upgrade_data.get('model', 'Unknown')}`\n"
            f"• **จุดเด่น / เหตุผล:** {upgrade_data.get('reason', 'ไม่ระบุเหตุผล')}\n"
            f"• **คะแนนทดสอบความเป๊ะ (Sandbox):** {upgrade_data.get('score', 0)}/100\n"
            f"• **ขอบเขตการใช้งาน:** {upgrade_data.get('action', 'ใช้งานทั่วไป')}\n\n"
            f"🛠️ **สิ่งที่นายท่านต้องทำหากอนุมัติ:**\n"
            f"1. เปิดไฟล์ `04_scripts/ai_model_registry.py`\n"
            f"2. แก้ไขชื่อโมเดลในตัวแปรสวิตช์หลักให้ตรงกับตัวที่แนะนำด้านบน\n"
            f"3. ทำการ Git Push ขึ้น Server เป็นอันเสร็จพิธีครับพ้ม!"
        )
        
        # ส่งการ์ดแจ้งเตือนสีแดงเด่นๆ ไปแสดงผลที่หน้าจอเว็บ Portal หลัก
        return self.publish_insight(
            author_team="AI_Evolution_BU",
            topic="📌 [คำขออนุมัติอัปเกรดสมองกลระบบ]",
            insight_data={
                "best_tools": [{"name": "Sandbox Auto-Tester"}, {"name": "Registry Dynamic Gate"}],
                "conclusion": insight_content
            }
        )

    def get_all_insights(self) -> list:
        """ ดึงรายงานทั้งหมดเพื่อส่งออกไปแสดงผลบนหน้าเว็บพอร์ตเทิล """
        # หากยังไม่มีข้อมูลเลย ให้แสดงข้อมูลต้อนรับเริ่มต้น
        if not self.insights_db:
            return [{
                "id": 0,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "author": "Base44_Core_System",
                "topic": "ยินดีต้อนรับเข้าสู่ระบบจัดการ AI อัจฉริยะ",
                "best_tools": [{"name": "System Engine V2"}],
                "conclusion": "ขณะนี้ระบบฐานทัพ AI และสวิตช์ควบคุมกลางพร้อมใช้งานแล้ว รอรับรายงานคิดสดได้เลยครับพ้ม!"
            }]
        return self.insights_db

shared_knowledge = SharedKnowledge()