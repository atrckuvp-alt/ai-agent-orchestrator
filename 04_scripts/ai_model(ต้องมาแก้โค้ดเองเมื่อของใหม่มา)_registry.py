# 04_scripts/ai_model_registry.py
import os

class AIModelRegistry:
    def __init__(self):
        # ==========================================================
        # 🕹️ [MASTER SWITCH] แก้ไขจุดนี้จุดเดียวเพื่อเปลี่ยนโมเดลทั้งระบบ
        # ==========================================================
        # โมเดลสำหรับการวิเคราะห์การตลาด (ดร.แสงสุข Framework)
        self.MARKETING_MODEL = "gemini-2.0-flash" 
        
        # โมเดลสำหรับการสร้างคอนเทนต์และสคริปต์ (เน้นความเร็ว)
        self.CONTENT_MODEL = "llama-3.3-70b-versatile" # รันบน Groq หรือ OpenRouter
        
        # โมเดลสำหรับการเขียนโค้ดและงานวิจัยเทคนิค
        self.CODING_MODEL = "gemini-2.0-flash"
        # ==========================================================

    def get_config(self, bu_type="marketing"):
        """ ฟังก์ชันแจกจ่ายคีย์และชื่อโมเดลให้แต่ละ BU ตามที่นายท่านเลือก """
        if bu_type == "marketing":
            model = self.MARKETING_MODEL
        elif bu_type == "content":
            model = self.CONTENT_MODEL
        else:
            model = self.CODING_MODEL

        # Logic การแมตช์ชื่อโมเดลกับ Provider (ระบบจะเลือกใช้ Key ที่ถูกต้องอัตโนมัติ)
        if "gemini" in model:
            return {"provider": "google", "key": os.getenv("GEMINI_API_KEY"), "model": model}
        elif "llama" in model or "mixtral" in model:
            return {"provider": "groq", "key": os.getenv("GROQ_API_KEY"), "model": model}
        elif "deepseek" in model:
            return {"provider": "deepseek", "key": os.getenv("DEEPSEEK_API_KEY"), "model": model}
        else:
            # กรณีโมเดลจากค่ายอื่นๆ ให้วิ่งผ่าน OpenRouter เป็นหลัก
            return {"provider": "openrouter", "key": os.getenv("OPENROUTER_API_KEY"), "model": model}

model_registry = AIModelRegistry()