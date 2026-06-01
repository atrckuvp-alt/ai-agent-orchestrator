import json
import logging
import sys
from pathlib import Path

# เพิ่ม path เพื่อให้ import ได้ถูกต้อง
sys.path.append(str(Path(__file__).resolve().parents[0]))

from provider_router import provider_router
from user_memory import user_memory

logger = logging.getLogger(__name__)

class IntentRouter:
    async def route_intent_with_memory(self, text: str, user_id: int) -> dict:
        """
        วิเคราะห์เจตนา (Intent) ของผู้ใช้โดยเชื่อมโยงกับความจำล่าสุดตามโครงสร้าง intent_routing.md
        """
        # ดึงบริบทเดิมจาก Memory
        mem_ctx = user_memory.get_context(user_id)
        past_intent = mem_ctx.get("current_intent", "general")
        past_summary = mem_ctx.get("summary_context", "ไม่มีประวัติก่อนหน้า")

        prompt = f"""
        คุณคือตัวคัดกรองเจตนาความต้องการขั้นสูง (Intent Router) หน้าที่ของคุณคือวิเคราะห์ข้อความล่าสุดจากผู้ใช้
        โดยพิจารณาร่วมกับ "ประวัติเจตนาเดิมและเรื่องที่คุยค้างไว้" เพื่อหาว่าเขาต้องการสั่งงานข้อใดตามกฎของ intent_routing.md
        
        กฎการเลือก Intent ID (ตามข้อกำหนด):
        - "run_orchestrator" : สั่งเปิดระบบประมวลผล ค้นหา เปรียบเทียบ AI Model (มักมีคีย์เวิร์ด --mock, --api, รันออร์เคสเตรเตอร์)
        - "oss_research" : สั่งค้นคว้าและทำรายงานเครื่องมือ Open-Source แยกตามหมวดหมู่ (เช่น ค้นคว้า, วิจัย, หา tools open source)
        - "cost_optimization" : ชุดคำสั่งวิเคราะห์ ประเมิน หรือคำนวณต้นทุนระบบ/เซิร์ฟเวอร์
        - "show_menu" : สั่งแสดงเมนูหลัก สลับหน้าจอคอนโซล สั่งยกเลิก หรือขอดูเมนู

        ---
        [บริบทความจำเดิมของผู้ใช้ ID: {user_id}]
        - เจตนาล่าสุดก่อนหน้านี้: {past_intent}
        - เรื่องที่สรุปค้างไว้: {past_summary}
        ---
        [ข้อความล่าสุดจากผู้ใช้]: "{text}"

        คำแนะนำพิเศษ: หากข้อความล่าสุดเป็นคำขยายความสั้นๆ (เช่น "เอาที่เป็น open source นะ", "ขอแบบฟรีด้วย") 
        และไม่ได้เปลี่ยนเรื่อง ให้พิจารณาตอบเป็น Intent เดิมจากบริบทความจำ เพื่อความต่อเนื่องในการทำงาน

        ส่งผลลัพธ์กลับมาเป็น JSON Object รูปแบบนี้เท่านั้น (ห้ามมีคำอธิบายอื่นนอก JSON):
        {{
            "intent": "ชื่อ Intent ที่เลือก (เลือกเฉพาะ: run_orchestrator, oss_research, cost_optimization, show_menu เท่านั้น)",
            "confidence": 0.00 ถึง 1.00,
            "objective": "ประโยคเป้าหมายที่แท้จริงที่รวมเอาบริบทความจำเดิมเข้ากับข้อความล่าสุดแล้วเพื่อให้ระบบประมวลผลต่อได้"
        }}
        """

        try:
            # ใช้ Fast Tier (เน้นความเร็วในการจำแนกเจตนา)
            ai_response = await provider_router.request_llm(prompt, tier="fast")
            cleaned_json = ai_response.replace("```json", "").replace("```", "").strip()
            result = json.loads(cleaned_json)
            logger.info(f"🎯 [Intent Router] Resolved to: {result.get('intent')} with context")
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ [Intent Router Fallback] AI คัดกรองไม่สำเร็จเนื่องจาก: {e}. ใช้สถิติคัดกรองเบื้องต้นแทน.")
            # ตรรกะ Fallback แบบ Static Rule
            lower_text = text.lower()
            if any(k in lower_text for k in ["วิจัย", "research", "oss", "open source"]):
                return {"intent": "oss_research", "confidence": 0.70, "objective": text}
            elif any(k in lower_text for k in ["ต้นทุน", "cost", "ราคา", "ประหยัด"]):
                return {"intent": "cost_optimization", "confidence": 0.70, "objective": text}
            elif any(k in lower_text for k in ["run", "รัน", "orchestrator"]):
                return {"intent": "run_orchestrator", "confidence": 0.70, "objective": text}
            else:
                return {"intent": "show_menu", "confidence": 0.50, "objective": text}

intent_router = IntentRouter()