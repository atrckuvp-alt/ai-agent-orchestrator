# Complete file: 04_scripts/growth_marketing_orchestrator.py
import os
import requests

class MarketingAgent:
    def __init__(self, api_keys: dict):
        self.api_keys = api_keys

    def execute_marketing_analysis(self, topic: str, core_skill: str, segmentation_skill: str) -> str:
        """ [ลูกทีมที่ 1 - AI การตลาด] วิเคราะห์แผนผ่านระบบสลับค่ายอัตโนมัติ (Gemini -> DeepSeek -> OpenRouter) """
        print(f"📊 [Marketing Agent] เริ่มการวิเคราะห์กลยุทธ์สำหรับ: '{topic}'...")

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

        # 🔄 ยุทธศาสตร์สลับค่ายชั้นที่ 1: ลองใช้ Gemini คีย์หลัก
        if self.api_keys.get("gemini_primary"):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_keys['gemini_primary']}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
                if res.status_code == 200:
                    return res.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                print(f"⚠️ [Failover] Gemini คีย์หลักขัดข้อง: {e} -> สลับไปคีย์สำรอง")

        # 🔄 ยุทธศาสตร์สลับค่ายชั้นที่ 2: ลองใช้ Gemini คีย์สำรอง
        if self.api_keys.get("gemini_backup"):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_keys['gemini_backup']}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
                if res.status_code == 200:
                    return res.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                print(f"⚠️ [Failover] Gemini คีย์สำรองขัดข้อง -> สลับไป DeepSeek")

        # 🔄 ยุทธศาสตร์สลับค่ายชั้นที่ 3: ดึงกำลังพลจาก DeepSeek เข้าช่วยงาน
        if self.api_keys.get("deepseek"):
            try:
                headers = {"Authorization": f"Bearer {self.api_keys['deepseek']}", "Content-Type": "application/json"}
                payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers, timeout=12)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"⚠️ [Failover] DeepSeek ขัดข้อง -> สลับไปกองหนุนสุดท้าย OpenRouter")

        # 🔄 ยุทธศาสตร์สลับค่ายชั้นที่ 4: ค่ายสุดท้าย OpenRouter ด่านหน้ากันระบบล่ม
        if self.api_keys.get("openrouter"):
            try:
                headers = {"Authorization": f"Bearer {self.api_keys['openrouter']}", "Content-Type": "application/json"}
                payload = {"model": "google/gemini-2.5-flash", "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=12)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception:
                pass

        return "📊 **[Marketing Agent Mode สำรอง]** แผนการตลาดคิดสด: ชูจุดขายพรีเมียม ไม่เน้นตัดราคา มุ่งเจาะ Pain Point กลุ่ม Niche กำลังซื้อสูง (เนื่องจาก API ทุกค่ายเชื่อมต่อไม่สำเร็จ)"


class ContentCreatorAgent:
    def __init__(self, api_keys: dict):
        self.api_keys = api_keys

    def generate_content_plan(self, topic: str, marketing_insight: str, tactics_skill: str, is_daily_job: bool = False) -> str:
        """ [ลูกทีมที่ 2 - AI นักครีเอทีฟ] รังสรรค์สคริปต์ความเร็วแสง (Groq -> Gemini -> OpenRouter) """
        print(f"🎬 [Content Creator Agent] กำลังทำแผนสื่อสารและไอเดียคอนเทนต์สำหรับ: '{topic}'...")

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

        # ⚡ สปีดสายฟ้าชั้นที่ 1: ดึง Groq (Llama-3) มาปั่นสคริปต์ด้วยความเร็วแสง
        if self.api_keys.get("groq"):
            try:
                headers = {"Authorization": f"Bearer {self.api_keys['groq']}", "Content-Type": "application/json"}
                payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=8)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception as e:
                print(f"⚠️ [Failover] Groq สปีดตกหรือติดขัด: {e} -> ส่งต่อให้พี่ใหญ่ Gemini")

        # 🔄 สลับค่ายชั้นที่ 2: ให้พี่ใหญ่ Gemini ช่วยเคลียร์งานคอนเทนต์
        if self.api_keys.get("gemini_primary"):
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_keys['gemini_primary']}"
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
                if res.status_code == 200:
                    return res.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                pass

        # 🔄 สลับค่ายชั้นที่ 3: ตายรังที่ OpenRouter ป้องกันบอทค้าง
        if self.api_keys.get("openrouter"):
            try:
                headers = {"Authorization": f"Bearer {self.api_keys['openrouter']}", "Content-Type": "application/json"}
                payload = {"model": "meta-llama/llama-3-8b-instruct", "messages": [{"role": "user", "content": prompt}]}
                res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=10)
                if res.status_code == 200:
                    return res.json()['choices'][0]['message']['content']
            except Exception:
                pass

        return "🎬 **[Content Creator Mode สำรอง]** ไอเดียคอนเทนต์: เน้นเล่าเรื่อง Storytelling ดึง Pain Point แท้จริง ชวนให้หยุดดูใน 3 วินาทีแรก และพาเข้า Line OA (เนื่องจาก API คอนเทนต์ทุกค่ายไม่ตอบสนอง)"


class GrowthMarketingOrchestrator:
    def __init__(self):
        self.dr_sangsook_skills = {
            "strategy_core": "Niche Market & Premium Differentiation (สร้างความต่างในตลาดเฉพาะกลุ่ม ไม่แข่งสงครามราคา)",
            "segmentation": "Deep Segmentation (มองหา Pain Point ที่ซ่อนอยู่ของกลุ่มเป้าหมายขนาดเล็กแต่มีกำลังซื้อสูง)",
            "product_value": "Functional + Emotional Value (สินค้าต้องแก้ปัญหาได้จริง และแบรนด์ต้องมอบความรู้สึกพรีเมียม)",
            "marketing_tactics": "Word-of-Mouth & Storytelling (ใช้การบอกต่อจากผู้ใช้จริงและการเล่าเรื่องที่กระทบใจ ไม่เน้นงบโฆษณาหว่านแห)"
        }
        
        # 📂 รวบรวมคลังแสง API ทั้ง 4 ค่ายจาก .env ของนายท่านมาจัดทัพ
        self.api_keys = {
            "gemini_primary": os.getenv("GEMINI_API_KEY"),
            "gemini_backup": os.getenv("GEMINI_BACKUP_API_KEY"),
            "deepseek": os.getenv("DEEPSEEK_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY"),
            "openrouter": os.getenv("OPENROUTER_API_KEY")
        }
        print(f"📡 [Base44 Core Engine] คลังแสงสแตนบาย -> Gemini(2) | DeepSeek(1) | Groq(1) | OpenRouter(1)")

        self.marketing_agent = MarketingAgent(self.api_keys)
        self.content_agent = ContentCreatorAgent(self.api_keys)

    def generate_strategic_plan(self, topic: str, is_daily_job: bool = False) -> dict:
        """ ผู้จัดการใหญ่คุมงาน จ่ายบรีฟ และประสานงานโมเดลข้ามค่ายไร้รอยต่อ """
        print(f"🧠 [Orchestrator] เริ่มทำงานแบบกระจายศูนย์ข้ามเครือข่าย AI กับผลิตภัณฑ์: '{topic}'")
        
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
            f"💡 **[กลั่นกรองผ่านระบบสลับค่ายอัจฉริยะ Multi-Cloud AI Engine]**\n\n"
            f"{marketing_report}\n\n"
            f"────────────────\n\n"
            f"{content_report}\n\n"
            f"🏆 **ยึดมั่นคุณค่าแบรนด์พรีเมียม:** {self.dr_sangsook_skills['product_value']}"
        )
        
        best_tools = [
            {"name": "Cross-AI Multi-Cloud Router Engine"},
            {"name": "Line OA Premium CRM Gate"},
            {"name": f"Base44 Quad-Core Automated Network ({topic})"}
        ]

        return {
            "best_tools": best_tools,
            "conclusion": combined_conclusion
        }

growth_marketing_orchestrator = GrowthMarketingOrchestrator()