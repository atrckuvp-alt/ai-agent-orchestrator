# Complete file: 04_scripts/growth_marketing_orchestrator.py
import os
import sys
import requests

# 🔌 [Senior Path Injection] บังคับให้ระบบมองเห็นไฟล์ทั้งหมดในโฟลเดอร์นี้เพื่อแก้ปัญหาเลข 04_
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# ตอนนี้สามารถ import ตรง ๆ ได้เลย ไม่ติดบั๊กทางเดินไฟล์แล้วครับ
from ai_model_registry import model_registry  

class MarketingAgent:
    def execute_marketing_analysis(self, topic: str, core_skill: str, segmentation_skill: str) -> str:
        """ [ลูกทีมที่ 1 - AI การตลาด] วิเคราะห์แผนผ่านระบบสลับค่าย โดยเช็กโมเดลอนุมัติจากสวิตช์กลาง """
        print(f"📊 [Marketing Agent] เริ่มการวิเคราะห์กลยุทธ์สำหรับ: '{topic}'...")

        config = model_registry.get_config("marketing")
        active_model = config["model"]
        active_key = config["key"]
        provider = config["provider"]

        prompt = f"""
        คุณคือผู้เชี่ยวชาญด้าน Growth Marketing ระดับโลก ที่ซึมซับกรอบแนวคิดธุรกิจของ เภสัชกร ดร.แสงสุข พิทยานุกุล อย่างทะลุปรุโปร่ง
        จงวิเคราะห์กลยุทธ์การตลาดและแผนปั๊มเงินสำหรับผลิตภัณฑ์/ธุรกิจต่อไปนี้: "{topic}"
        
        โดยมีข้อบังคับว่าต้องใช้หลักยุทธศาสตร์สำคัญ 2 ข้อนี้ในการคิด:
        1. Core Strategy: {core_skill}
        2. Customer Target: {segmentation_skill}
        
        รูปแบบคำตอบ (ตอบเป็นภาษาไทย เขียนสรุปกระชับ คมคาย เข้าใจง่าย ไม่เอาน้ำ):
        📊 **[Marketing Agent Analysis Report]**
        • **ยุทธศาสตร์การแข่งขัน:** (สรุปสั้นๆ ว่าจะสร้างความต่างอย่างไรในตลาดเฉพาะกลุ่มนี้)
        • **การเจาะกลุ่มเป้าหมาย (Deep Segmentation):** (ระบุ Pain Point ที่ซ่อนอยู่ของกลุ่มลูกค้าพรีเมียมตัวจริง)
        • **แผนการปั๊มเงิน (Product Execution):** (บอก Action Plan 1-2 ข้อชัดๆ ว่าจะดึงเงินออกจากกระเป๋าเขาอย่างไรโดยไม่แข่งลดราคา)
        """

        if provider == "google" and active_key:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{active_model}:generateContent?key={active_key}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
                if res.status_code == 200:
                    return res.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                print(f"⚠️ [Failover] สวิตช์หลัก Google มีปัญหา: {e} -> ดีดไปเข้า OpenRouter")

        elif provider == "deepseek" and active_key:
            try:
                headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"}
                payload = {"model": active_model, "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers, timeout=12)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"⚠️ [Failover] สวิตช์หลัก DeepSeek มีปัญหา: {e} -> ดีดไปเข้า OpenRouter")

        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            try:
                fallback_model = "google/gemini-2.5-flash" if provider == "google" else "deepseek/deepseek-chat"
                headers = {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"}
                payload = {"model": fallback_model, "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=12)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception:
                pass

        return f"📊 **[Marketing Agent Mode สำรอง]** แผนกลยุทธ์พรีเมียมสำหรับ '{topic}' มุ่งเน้นการสร้าง Value โดยไม่ตัดราคา (รันบนระบบสำรองฐานราก)"


class ContentCreatorAgent:
    def generate_content_plan(self, topic: str, marketing_insight: str, tactics_skill: str, is_daily_job: bool = False) -> str:
        """ [ลูกทีมที่ 2 - AI นักครีเอทีฟ] รังสรรค์สคริปต์คอนเทนต์ เช็กโมเดลจากสวิตช์ส่วนกลาง """
        print(f"🎬 [Content Creator Agent] กำลังทำแผนสื่อสารและไอเดียคอนเทนต์สำหรับ: '{topic}'...")

        config = model_registry.get_config("content")
        active_model = config["model"]
        active_key = config["key"]
        provider = config["provider"]

        mode_text = "โหมดสุ่มไอเดียแปลกใหม่ประจำวัน" if is_daily_job else "โหมดแผนงานคอนเทนต์หลักประจำแคมเปญ"
        prompt = f"""
        คุณคือผู้กำกับคอนเทนต์และมือเขียนบทวิดีโอสั้นระดับพรีเมียม
        จงนำ 'บทวิเคราะห์การตลาดด้านล่างนี้' ไปแตกย่อยเป็นแผนงานไอเดียคลิปสั้นสำหรับสินค้า: "{topic}" ({mode_text})
        
        กรอบยุทธศาสตร์การสื่อสารที่ต้องฝังลงไป: {tactics_skill}
        บทวิเคราะห์จากฝ่ายการตลาดที่ต้องนำไปต่อยอด:
        {marketing_insight}
        
        รูปแบบคำตอบ (ตอบเป็นภาษาไทย เขียนกระตุ้นอารมณ์ น่าสนใจ ดึงดูดสายตาคนดูใน 3 วินาทีแรก):
        🎬 **[Content Creator Execution Plan]**
        • **ยุทธศาสตร์การสื่อสาร:** (แนวทางการเล่าเรื่องหรือ Hook ล่อลูกค้าใน 3 วินาทีแรก)
        • **มุมมองเนื้อหา (Content Hook & Storyline):** (เขียนโครงเรื่อง/สคริปต์สั้นๆ 1 ไอเดียที่กระตุ้นพลังบอกต่อ)
        • **Conversion Funnel:** (วิธีดึงคนดูจากคลิปสั้นให้กดทัก Line OA เพื่อปิดการขายหรือสมัครสมาชิก)
        """

        if provider == "groq" and active_key:
            try:
                headers = {"Authorization": f"Bearer {active_key}", "Content-Type": "application/json"}
                payload = {"model": active_model, "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=8)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"⚠️ [Failover] โครงข่าย Groq ติดขัด: {e} -> ส่งไปพึ่งพากองหนุน OpenRouter")

        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            try:
                headers = {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"}
                payload = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=10)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception:
                pass

        return "🎬 **[Content Creator Mode สำรอง]** ไอเดียคอนเทนต์: เน้นเล่าเรื่อง Storytelling ชวนให้หยุดดูใน 3 วินาทีแรก และพาเข้าระบบปิดการขาย Line OA"


class GrowthMarketingOrchestrator:
    def __init__(self):
        self.dr_sangsook_skills = {
            "strategy_core": "Niche Market & Premium Differentiation (สร้างความต่างในตลาดเฉพาะกลุ่ม ไม่แข่งสงครามราคา)",
            "segmentation": "Deep Segmentation (มองหา Pain Point ที่ซ่อนอยู่ของกลุ่มเป้าหมายขนาดเล็กแต่มีกำลังซื้อสูง)",
            "product_value": "Functional + Emotional Value (สินค้าต้องแก้ปัญหาได้จริง และแบรนด์ต้องมอบความรู้สึกพรีเมียม)",
            "marketing_tactics": "Word-of-Mouth & Storytelling (ใช้การบอกต่อจากผู้ใช้จริงและการเล่าเรื่องที่กระทบใจ ไม่เน้นงบโฆษณาหว่านแห)"
        }
        print(f"📡 [Base44 Centralized Switch Engine] ดึงแผนควบคุมจาก Model Registry เรียบร้อยแล้ว")

        self.marketing_agent = MarketingAgent()
        self.content_agent = ContentCreatorAgent()

    def generate_strategic_plan(self, topic: str, is_daily_job: bool = False) -> dict:
        """ ผู้จัดการใหญ่คุมงาน จ่ายบรีฟ และประสานงานโมเดลควบคุมข้ามเครือข่าย """
        print(f"🧠 [Orchestrator] เริ่มทำงานผ่านสวิตช์กลาง AI Engine กับผลิตภัณฑ์: '{topic}'")
        
        marketing_report = self.marketing_agent.execute_marketing_analysis(
            topic=topic,
            core_skill=self.dr_sangsook_skills["strategy_core"],
            segmentation_skill=self.dr_sangsook_skills["segmentation"]
        )
        
        content_report = self.content_agent.generate_content_plan(
            topic=topic,
            marketing_insight=marketing_report,
            tactics_skill=self.dr_sangsook_skills["marketing_tactics"],
            is_daily_job=is_daily_job
        )
        
        combined_conclusion = (
            f"💡 **[กลั่นกรองผ่านระบบศูนย์กลางควบคุม AI Model Registry]**\n\n"
            f"{marketing_report}\n\n"
            f"────────────────\n\n"
            f"{content_report}\n\n"
            f"🏆 **ยึดมั่นคุณค่าแบรนด์พรีเมียม:** {self.dr_sangsook_skills['product_value']}"
        )
        
        best_tools = [
            {"name": f"Registry Controlled Engine ({model_registry.MARKETING_MODEL})"},
            {"name": "Line OA Premium CRM Gate"},
            {"name": f"Base44 Evolution-Ready Base ({topic})"}
        ]

        return {
            "best_tools": best_tools,
            "conclusion": combined_conclusion
        }

growth_marketing_orchestrator = GrowthMarketingOrchestrator()