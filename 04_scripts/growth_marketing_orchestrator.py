# Complete file: 04_scripts/growth_marketing_orchestrator.py
import json
import random

class MarketingAgent:
    def execute_marketing_analysis(self, topic: str, core_skill: str, segmentation_skill: str) -> str:
        """ [ลูกทีมที่ 1] วิเคราะห์การตลาดเชิงลึก แยกตามประเภทสินค้าแบบ Dynamic """
        print(f"📊 [Marketing Agent] กำลังวิเคราะห์ตลาดสำหรับโจทย์: '{topic}'...")
        
        # ปรับการวิเคราะห์ให้ยืดหยุ่นตามสินค้าที่ส่งเข้ามา
        if "ข้าวสาร" in topic:
            product_insight = "เจาะกลุ่มคนเมืองที่อาศัยในคอนโดและรักสุขภาพด้วย 'ข้าวสารพรีเมียมขนาดทดลองทาน' ดัชนีน้ำตาลต่ำ ป้องกันมอดด้วยระบบสุญญากาศ 100%"
        elif "แชมพู" in topic or "ผม" in topic:
            product_insight = "เจาะกลุ่มวัยทำงานที่มีปัญหาผมร่วงชะงักจากความเครียด ด้วย 'แชมพูสมุนไพรออร์แกนิกสกัดเย็น' ชูจุดเด่นลดสารเคมีตกค้างบนหนังศีรษะขจัดรังแค"
        else:
            product_insight = f"วิเคราะห์กลยุทธ์ Blue Ocean สำหรับโปรดักก์ยุคใหม่ เน้นแก้ไข Pain Point เฉพาะกลุ่มที่ยังมีคู่แข่งน้อย"

        analysis_result = (
            f"📊 **[Marketing Agent Analysis Report]**\n"
            f"• **ยุทธศาสตร์การแข่งขัน:** {core_skill}\n"
            f"• **การเจาะกลุ่มเป้าหมาย (Deep Segmentation):** {segmentation_skill}\n"
            f"• **แผนการปั๊มเงิน (Product Execution):** {product_insight}"
        )
        return analysis_result

class ContentCreatorAgent:
    def __init__(self):
        # 📚 คลังมุมมองไอเดียคอนเทนต์แบ่งแยกตามหมวดหมู่สินค้า
        self.rice_angles = [
            "⚠️ ไอเดียแก้อาการ 'ข้าวบูดคาหม้อ' พร้อมวิธีแก้ด้วยการเลือกสายพันธุ์ข้าวออร์แกนิกหุงขึ้นหม้อ",
            "🌾 เปิดเผยการเดินทางของ 'เมล็ดข้าวพรีเมียม' จากผืนนาอินทรีย์ที่เพาะปลูกด้วยความรักสู่จานข้าวคอนโดคุณ",
            "🥗 รีวิวสูตรลับ 'ข้าวผัดสุขภาพแคลอรีต่ำ' สำหรับพนักงานออฟฟิศที่ไม่มีเวลาออกกำลังกาย"
        ]
        self.shampoo_angles = [
            "🤯 ตื่นมาผมร่วงเต็มหมอน? แฉ 3 พฤติกรรมมนุษย์ออฟฟิศที่ทำร้ายหนังศีรษะโดยไม่รู้ตัว",
            "🌿 เปิดสูตรลับสมุนไพรไทย 4 ชนิดที่ ดร.แนะว่าช่วยล็อครากผมให้แข็งแรงหนาดกดำขึ้น 2 เท่า",
            "🧴 รีวิวสลับขวด: แชมพูเคมีทั่วไป vs แชมพูออร์แกนิกสกัดเย็น สัมผัสต่างกันอย่างไรใน 7 วัน"
        ]

    def generate_content_plan(self, topic: str, marketing_insight: str, tactics_skill: str, is_daily_job: bool = False) -> str:
        """ [ลูกทีมที่ 2] แปลงผลวิเคราะห์เป็นสคริปต์เนื้อหาแยกตามหมวดสินค้า """
        print(f"🎬 [Content Creator Agent] กำลังรังสรรค์คอนเทนต์สำหรับ: '{topic}'...")
        
        # เลือกคลังไอเดียให้ตรงกับสินค้าที่ระบุมา
        if "แชมพู" in topic or "ผม" in topic:
            angles_pool = self.shampoo_angles
            default_main = "เจาะลึกสตอรี่ไลน์ซีรีส์คลิปสั้น 'คืนชีพให้เส้นผมในวันที่งานรุมเร้า' สะท้อนชีวิตคนทำงานชานเมือง"
        else:
            angles_pool = self.rice_angles
            default_main = "เจาะลึกสตอรี่ไลน์ซีรีส์คลิปสั้น 3 ตอน 'ความลับของข้าวคำแรกตอนเช้า' เพื่อกระทบใจคนทำงานเมือง"

        if is_daily_job:
            selected_angle = random.choice(angles_pool)
            content_detail = f"📢 **[สุ่มหยิบไอเดียประจำวันสำเร็จ]**\n🎯 มุมมองเนื้อหาวันนี้: {selected_angle}"
        else:
            content_detail = f"🎯 แผนงานคอนเทนต์หลัก: {default_main}"

        plan_result = (
            f"🎬 **[Content Creator Execution Plan]**\n"
            f"• **ยุทธศาสตร์การสื่อสาร:** {tactics_skill}\n"
            f"• {content_detail}\n"
            f"• **Conversion Funnel:** ผลิตสื่อ Short-form (TikTok/Reels) พร้อมระบบให้ลงทะเบียนรับสินค้าขนาดเดินทาง (Travel Size) ฟรี เพื่อแปลงผู้ชมขาจรเป็นผู้ซื้อในระบบ CRM บน Line OA"
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
        """ ผู้จัดการรับงานจ่ายต่อแบบ Dynamic ขนานกันได้ทุกสินค้า """
        print(f"🧠 [Growth Marketing Orchestrator] เริ่มทำงานกับโจทย์: '{topic}' (โหมดประจำวัน: {is_daily_job})")
        
        # 1. ส่งงานให้ Marketing วิเคราะห์กลยุทธ์เฉพาะสินค้า
        marketing_report = self.marketing_agent.execute_marketing_analysis(
            topic=topic,
            core_skill=self.dr_sangsook_skills["strategy_core"],
            segmentation_skill=self.dr_sangsook_skills["segmentation"]
        )
        
        # 2. ส่งต่อให้ Content ครีเอทคอนเทนต์ให้ตรงกลุ่มสินค้า
        content_report = self.content_agent.generate_content_plan(
            topic=topic,
            marketing_insight=marketing_report,
            tactics_skill=self.dr_sangsook_skills["marketing_tactics"],
            is_daily_job=is_daily_job
        )
        
        # 3. รวมร่างข้อมูลความสำเร็จ
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
            {"name": f"Base44 Core Analyzer ({topic})"}
        ]

        return {
            "best_tools": best_tools,
            "conclusion": combined_conclusion
        }

growth_marketing_orchestrator = GrowthMarketingOrchestrator()