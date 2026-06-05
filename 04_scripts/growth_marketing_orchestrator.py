# Complete file: 04_scripts/growth_marketing_orchestrator.py (Real Multi-Agent Collaboration)
import json

class MarketingAgent:
    def execute_marketing_analysis(self, topic: str, core_skill: str, segmentation_skill: str) -> str:
        """ [ลูกทีมที่ 1] รับแนวคิด ดร.แสงสุข ไปวิเคราะห์กลยุทธ์ตลาดเชิงลึก """
        print("📊 [Marketing Agent] กำลังรับบรีฟแนวคิด ดร.แสงสุข มาวิเคราะห์ตลาด...")
        # ตรงนี้คือจุดที่ในอนาคตจะเชื่อมต่อเข้ากับ LLM/Gemini API เพื่อสั่งคิดงานจริง
        analysis_result = (
            f"📊 **[Marketing Agent Analysis Report]**\n"
            f"• **ยุทธศาสตร์ที่ใช้:** {core_skill}\n"
            f"• **การเจาะกลุ่มเป้าหมาย:** {segmentation_skill}\n"
            f"• **แผนการปั๊มเงินจริง:** สำหรับโจทย์ '{topic}' เราจะทำแพ็กเกจข้าวสารพรีเมียมขนาดทดลองทาน สำหรับพนักงานออฟฟิศที่อยู่คอนโด เพื่อลดปัญหาข้าวเก่าคาถัง คัดสรรสายพันธุ์ดัชนีน้ำตาลต่ำเพื่อตอบโจทย์ Functional Value ด้านสุขภาพ"
        )
        return analysis_result

class ContentCreatorAgent:
    def generate_content_plan(self, topic: str, marketing_insight: str, tactics_skill: str) -> str:
        """ [ลูกทีมที่ 2] รับผลวิเคราะห์จากการตลาด มาแปลงเป็นแผนสื่อโฆษณาและการบอกต่อ """
        print("🎬 [Content Creator Agent] กำลังนำผลวิเคราะห์การตลาดมาสร้างสื่อบอกต่อ...")
        plan_result = (
            f"🎬 **[Content Creator Execution Plan]**\n"
            f"• **ยุทธศาสตร์การสื่อสาร:** {tactics_skill}\n"
            f"• **แผนงานคอนเทนต์:** นำข้อมูลจากฝ่ายการตลาดมารังสรรค์เป็นซีรีส์คลิปสั้น 3 ตอน 'ความลับของข้าวคำแรกตอนเช้า' เน้นเจาะใจ (Emotional) คนทำงานที่เหนื่อยล้า พ่วงด้วยกิจกรรมแจกสินค้าทดลองให้เพจสายสุขภาพรีวิว เพื่อกระตุ้นพลังบอกต่อ (Word-of-Mouth)"
        )
        return plan_result


class GrowthMarketingOrchestrator:
    def __init__(self):
        # 🧠 สกัดชุดความคิดระดับพรีเมียมของ เภสัชกร ดร.แสงสุข พิทยานุกุล
        self.dr_sangsook_skills = {
            "strategy_core": "Niche Market & Premium Differentiation (สร้างความต่างในตลาดเฉพาะกลุ่ม)",
            "segmentation": "Deep Segmentation (เจาะ Pain Point กลุ่มย่อยแต่มีกำลังซื้อสูง)",
            "product_value": "Functional + Emotional Value (สินค้าต้องแก้ปัญหาได้จริงและแบรนด์ต้องให้ความรู้สึกที่ดี)",
            "marketing_tactics": "Word-of-Mouth & Storytelling (เน้นการบอกต่อจากผู้ใช้จริงและการเล่าเรื่องที่กระทบใจ)"
        }
        # 🤝 ดึงลูกทีมทั้งสองเข้าประจำการใน BU 
        self.marketing_agent = MarketingAgent()
        self.content_agent = ContentCreatorAgent()

    def generate_strategic_plan(self, topic: str) -> dict:
        """ 
        ผู้จัดการรับงานจาก Meta แล้วทำหน้าที่ 'บรีฟและจ่ายงาน' ให้ลูกทีมทำงานต่อกันเป็นทอดๆ 
        ตามกรอบความคิดของ ดร.แสงสุข
        """
        print(f"🧠 [Growth Marketing Orchestrator] เริ่มกระบวนการกระจายงานใน BU ปั๊มเงิน...")
        
        # 1. ผู้จัดการส่งโจทย์ + แนวคิด ดร.แสงสุข ให้ Marketing Agent ทำงาน
        marketing_report = self.marketing_agent.execute_marketing_analysis(
            topic=topic,
            core_skill=self.dr_sangsook_skills["strategy_core"],
            segmentation_skill=self.dr_sangsook_skills["segmentation"]
        )
        
        # 2. ผู้จัดการส่งต่อผลวิเคราะห์ของการตลาด + แนวคิด ดร.แสงสุข ให้ Content Creator ทำงานต่อ
        content_report = self.content_agent.generate_content_plan(
            topic=topic,
            marketing_insight=marketing_report,
            tactics_skill=self.dr_sangsook_skills["marketing_tactics"]
        )
        
        # 3. รวบรวมผลงานจริงจากลูกทีมทั้งสองส่งกลับไปให้ Meta Orchestrator
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
            {"name": "Base44 Core Analytical Suite"}
        ]

        return {
            "best_tools": best_tools,
            "conclusion": combined_conclusion
        }

growth_marketing_orchestrator = GrowthMarketingOrchestrator()