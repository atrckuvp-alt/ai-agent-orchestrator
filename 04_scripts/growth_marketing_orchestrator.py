# Complete file: 04_scripts/growth_marketing_orchestrator.py
import json
import random

class MarketingAgent:
    def execute_marketing_analysis(self, topic: str, core_skill: str, segmentation_skill: str) -> str:
        """ [ลูกทีมที่ 1] วิเคราะห์การตลาดเชิงลึก """
        print("📊 [Marketing Agent] กำลังวิเคราะห์ตลาดตามกรอบ ดร.แสงสุข...")
        analysis_result = (
            f"📊 **[Marketing Agent Analysis Report]**\n"
            f"• **ยุทธศาสตร์:** {core_skill}\n"
            f"• **การเจาะกลุ่มเป้าหมาย:** {segmentation_skill}\n"
            f"• **แผนการปั๊มเงิน:** เจาะกลุ่มคนเมืองที่อาศัยในคอนโดและรักสุขภาพด้วย 'ข้าวสารพรีเมียมขนาดทดลองทาน' ดัชนีน้ำตาลต่ำ ป้องกันมอดด้วยระบบสุญญากาศ 100%"
        )
        return analysis_result

class ContentCreatorAgent:
    def __init__(self):
        # 📚 คลังมุมมองไอเดียคอนเทนต์ประจำวัน (Daily Content Angle Pool) ตามกลยุทธ์บอกต่อของ ดร.แสงสุข
        self.content_angles = [
            "⚠️ ไอเดียแก้อาการ 'ข้าวบูดคาหม้อ' พร้อมวิธีแก้ด้วยการเลือกสายพันธุ์ข้าวออร์แกนิกหุงขึ้นหม้อ",
            "🌾 เปิดเผยการเดินทางของ 'เมล็ดข้าวพรีเมียม' จากผืนนาอินทรีย์ที่เพาะปลูกด้วยความรักสู่จานข้าวคอนโดคุณ",
            "🥗 รีวิวสูตรลับ 'ข้าวผัดสุขภาพแคลอรีต่ำ' สำหรับพนักงานออฟฟิศที่ไม่มีเวลาออกกำลังกาย",
            "💡 ความจริงที่โรงสีไม่เคยบอก: วิธีสังเกตข้าวสารสดใหม่ที่ไม่ใช่น้ำยาฆ่ามอด ยิ่งกินยิ่งสุขภาพดี",
            "🕒 ประหยัดเวลาหุงข้าวไป 15 นาที! เคล็ดลับการเตรียมข้าวกล้องนุ่มทานง่ายสำหรับคนตื่นสาย"
        ]

    def generate_content_plan(self, topic: str, marketing_insight: str, tactics_skill: str, is_daily_job: bool = False) -> str:
        """ [ลูกทีมที่ 2] แปลงผลวิเคราะห์เป็นสคริปต์เนื้อหา """
        print("🎬 [Content Creator Agent] กำลังรังสรรค์เนื้อหา...")
        
        # ถ้าระบบเรียกมาแบบอัตโนมัติประจำวัน ให้สุ่มหยิบมุมมองสดใหม่จากคลังไอเดียมาใช้งานทันที
        if is_daily_job:
            selected_angle = random.choice(self.content_angles)
            content_detail = f"📢 **[สุ่มหยิบไอเดียประจำวันสำเร็จ]**\n🎯 มุมมองเนื้อหาวันนี้: {selected_angle}"
        else:
            content_detail = f"🎯 แผนงานคอนเทนต์หลัก: เจาะลึกสตอรี่ไลน์ซีรีส์คลิปสั้น 3 ตอน 'ความลับของข้าวคำแรกตอนเช้า' เพื่อกระทบใจคนทำงานเมือง"

        plan_result = (
            f"🎬 **[Content Creator Execution Plan]**\n"
            f"• **ยุทธศาสตร์การสื่อสาร:** {tactics_skill}\n"
            f"• {content_detail}\n"
            f"• **Conversion Funnel:** ยิงคลิปสั้นสไตล์ Short-form ลง TikTok/Reels พร้อมฝังลิงก์รับกล่องสุ่มสินค้าทดลองฟรี เพื่อดึงลูกค้าเข้าฐานข้อมูลสมาชิกระยะยาวบน Line OA"
        )
        return plan_result


class GrowthMarketingOrchestrator:
    def __init__(self):
        self.dr_sangsook_skills = {
            "strategy_core": "Niche Market & Premium Differentiation (สร้างความต่างในตลาดเฉพาะกลุ่ม)",
            "segmentation": "Deep Segmentation (เจาะ Pain Point กลุ่มย่อยแต่มีกำลังซื้อสูง)",
            "product_value": "Functional + Emotional Value (สินค้าต้องแก้ปัญหาได้จริงและแบรนด์ต้องพรีเมียม)",
            "marketing_tactics": "Word-of-Mouth & Storytelling (เน้นการบอกต่อจากผู้ใช้จริงและการเล่าเรื่องที่กระทบใจ)"
        }
        self.marketing_agent = MarketingAgent()
        self.content_agent = ContentCreatorAgent()

    def generate_strategic_plan(self, topic: str, is_daily_job: bool = False) -> dict:
        """ ผู้จัดการรับงาน และส่งบรีฟให้ลูกทีมวิเคราะห์ทำงานต่อกันเป็นทอดๆ """
        print(f"🧠 [Growth Marketing Orchestrator] เริ่มทำงาน (โหมดประจำวันอัตโนมัติ: {is_daily_job})")
        
        # 1. ส่งงานให้ Marketing วิเคราะห์
        marketing_report = self.marketing_agent.execute_marketing_analysis(
            topic=topic,
            core_skill=self.dr_sangsook_skills["strategy_core"],
            segmentation_skill=self.dr_sangsook_skills["segmentation"]
        )
        
        # 2. ส่งต่อให้ Content ทำคอนเทนต์ประจำวัน
        content_report = self.content_agent.generate_content_plan(
            topic=topic,
            marketing_insight=marketing_report,
            tactics_skill=self.dr_sangsook_skills["marketing_tactics"],
            is_daily_job=is_daily_job
        )
        
        # 3. รวบรวมข้อมูลส่งกลับ
        combined_conclusion = (
            f"💡 **[ผ่านการกลั่นกรองโดยระบบ Multi-Agent Team]**\n\n"
            f"{marketing_report}\n\n"
            f"────────────────\n\n"
            f"{content_report}\n\n"
            f"🏆 **สรุปภาพรวมคุณค่าแบรนด์:** {self.dr_sangsook_skills['product_value']}"
        )
        
        best_tools = [
            {"name": "TikTok Shop Creator Affiliate Network"},
            {"name": "Line OA Subscription & CRM Automation"},
            {"name": "Base44 Daily Scheduler Server"}
        ]

        return {
            "best_tools": best_tools,
            "conclusion": combined_conclusion
        }

growth_marketing_orchestrator = GrowthMarketingOrchestrator()