# Complete file: 04_scripts/growth_marketing_orchestrator.py
import json
import random

class MarketingAgent:
    def execute_marketing_analysis(self, topic: str, core_skill: str, segmentation_skill: str) -> str:
        """ [ลูกทีมที่ 1] วิเคราะห์การตลาดเชิงลึก รองรับสินค้าแบบ Dynamic ทุกประเภท """
        print(f"📊 [Marketing Agent] กำลังวิเคราะห์กลยุทธ์ตลาดสำหรับโจทย์: '{topic}'...")
        
        # 💡 นี่คือจุดรับค่า Dynamic และโครงสร้างบรีฟ (Prompt Template) ที่จะส่งต่อให้ AI จริงในก้าวถัดไป
        # ในปัจจุบันระบบจะดึงชื่อสินค้าที่นายท่านพิมพ์มา แล้วประกอบเข้ากับกรอบแนวคิดของ ดร.แสงสุข โดยอัตโนมัติ
        analysis_result = (
            f"📊 **[Marketing Agent Analysis Report]**\n"
            f"• **ยุทธศาสตร์แบรนด์พรีเมียม:** {core_skill}\n"
            f"• **การเจาะกลุ่มตลาดเฉพาะ (Deep Segmentation):** {segmentation_skill}\n"
            f"• **แผนยุทธศาสตร์สินค้าของจริง:** สำหรับโจทย์ผลิตภัณฑ์ '{topic}' เราจะหลีกเลี่ยงการแข่งขันด้านราคาในตลาดแฮร์รี่หรือแมสทั่วไป แต่จะชูจุดเด่นด้าน Functional Value ที่พิสูจน์ได้ทางวิทยาศาสตร์/ธรรมชาติ ผสานดีไซน์มินิมอลเพื่อยกระดับ Emotional Value มัดใจกลุ่มเป้าหมายที่มีกำลังซื้อสูงและกำลังเผชิญ Pain Point นี้โดยตรง"
        )
        return analysis_result

class ContentCreatorAgent:
    def generate_content_plan(self, topic: str, marketing_insight: str, tactics_skill: str, is_daily_job: bool = False) -> str:
        """ [ลูกทีมที่ 2] แปลงผลวิเคราะห์การตลาดเป็นแผนงานคอนเทนต์บอกต่อสไตล์ Dynamic """
        print(f"🎬 [Content Creator Agent] กำลังรังสรรค์ไอเดียเนื้อหาสำหรับโจทย์: '{topic}'...")
        
        # คลังไอเดียแบบเปิดกว้าง (Dynamic Content Angle Pool) ที่สามารถนำไปประยุกต์ใช้ได้กับสินค้าทุกประเภทบนโลก
        dynamic_angles = [
            f"⚠️ แฉความจริงที่ตลาดไม่เคยบอก: เคล็ดลับและวิธีแก้ปัญหาเกี่ยวกับ '{topic}' ที่คนส่วนใหญ่ทำพลาดจนเสียเงินฟรี",
            f"🌿 เจาะลึกเบื้องหลังความใส่ใจ: การเดินทางของตัวแปรพรีเมียมใน '{topic}' ตั้งแต่แหล่งวัตถุดิบต้นกำเนิดอันบริสุทธิ์จนถึงมือคุณ",
            f"🕒 เปลี่ยนชีวิตให้ง่ายขึ้น 2 เท่า! รีวิวแนวทางการประยุกต์ใช้ '{topic}' สำหรับคนยุคใหม่ที่ตื่นสายและมีเวลาน้อย"
        ]

        if is_daily_job:
            selected_angle = random.choice(dynamic_angles)
            content_detail = f"📢 **[สุ่มหยิบไอเดียประจำวันสำเร็จ]**\n🎯 มุมมองเนื้อหาวันนี้: {selected_angle}"
        else:
            content_detail = f"🎯 แผนงานคอนเทนต์หลัก: เจาะลึกการสร้างคลิปสั้นซีรีส์ 3 ตอนในหมวด '{topic}' มุ่งเน้นการเล่าเรื่องเพื่อกระตุ้นอารมณ์ร่วม (Emotional Storytelling) และกระทบใจกลุ่มคนทำงาน"

        plan_result = (
            f"🎬 **[Content Creator Execution Plan]**\n"
            f"• **ยุทธศาสตร์การเข้าถึงกลุ่มเป้าหมาย:** {tactics_skill}\n"
            f"• {content_detail}\n"
            f"• **Conversion Funnel:** ผลิตสื่อ Short-form วิดีโอลง TikTok/Reels ดึงดูดความสนใจใน 3 วินาทีแรก แล้วใช้ระบบแจกสินค้าทดลอง/คูปองพิเศษ เพื่อดึงคนเข้าสู่ระบบสมัครสมาชิกรายเดือนอัตโนมัติบนฐานข้อมูล Line OA"
        )
        return plan_result


class GrowthMarketingOrchestrator:
    def __init__(self):
        # 🧠 สกัดคลังสมองและแนวคิดธุรกิจระดับครูของ เภสัชกร ดร.แสงสุข พิทยานุกุล เป็น Skill Set หลัก
        self.dr_sangsook_skills = {
            "strategy_core": "Niche Market & Premium Differentiation (สร้างความต่างในตลาดเฉพาะกลุ่ม ไม่แข่งสงครามราคา)",
            "segmentation": "Deep Segmentation (มองหา Pain Point ที่ซ่อนอยู่ของกลุ่มเป้าหมายขนาดเล็กแต่มีกำลังซื้อสูง)",
            "product_value": "Functional + Emotional Value (สินค้าต้องแก้ปัญหาได้จริง และแบรนด์ต้องมอบความรู้สึกพรีเมียม)",
            "marketing_tactics": "Word-of-Mouth & Storytelling (ใช้การบอกต่อจากผู้ใช้จริงและการเล่าเรื่องที่กระทบใจ ไม่เน้นงบโฆษณาหว่านแห)"
        }
        self.marketing_agent = MarketingAgent()
        self.content_agent = ContentCreatorAgent()

    def generate_strategic_plan(self, topic: str, is_daily_job: bool = False) -> dict:
        """ ผู้จัดการรับงาน Dynamic จากสมองกลาง แล้วส่งบรีฟงานให้ลูกทีมปฏิบัติการตามกรอบ ดร.แสงสุข """
        print(f"🧠 [Growth Marketing Orchestrator] เริ่มประมวลผลระบบทีมเวิร์คคู่ขนานกับสินค้า: '{topic}'")
        
        # 1. ส่งโจทย์สินค้าใดๆ + แนวคิด ดร.แสงสุข ให้การตลาดวิเคราะห์
        marketing_report = self.marketing_agent.execute_marketing_analysis(
            topic=topic,
            core_skill=self.dr_sangsook_skills["strategy_core"],
            segmentation_skill=self.dr_sangsook_skills["segmentation"]
        )
        
        # 2. ส่งต่อผลการตลาดให้ฝ่ายคอนเทนต์รังสรรค์สคริปต์ตามหมวดสินค้านั้นๆ
        content_report = self.content_agent.generate_content_plan(
            topic=topic,
            marketing_insight=marketing_report,
            tactics_skill=self.dr_sangsook_skills["marketing_tactics"],
            is_daily_job=is_daily_job
        )
        
        # 3. ประกอบข้อมูลแผนงานส่งกลับโครงสร้างหลัก
        combined_conclusion = (
            f"💡 **[ผ่านการกลั่นกรองโดยระบบ Multi-Agent Team - โหมด Dynamic Product]**\n\n"
            f"{marketing_report}\n\n"
            f"────────────────\n\n"
            f"{content_report}\n\n"
            f"🏆 **สรุปภาพรวมคุณค่าแบรนด์พรีเมียม:** {self.dr_sangsook_skills['product_value']}"
        )
        
        best_tools = [
            {"name": "TikTok Shop Creator Affiliate Network"},
            {"name": "Line OA CRM & Subscription Automation"},
            {"name": f"Base44 Smart Core Engine ({topic})"}
        ]

        return {
            "best_tools": best_tools,
            "conclusion": combined_conclusion
        }

growth_marketing_orchestrator = GrowthMarketingOrchestrator()