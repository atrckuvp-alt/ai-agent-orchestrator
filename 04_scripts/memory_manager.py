import json
import datetime as dt
from pathlib import Path
from provider_router import provider_router # ดึงตัวเราท์เตอร์ของคุณมาใช้

ROOT = Path(__file__).resolve().parents[1]
MEMORY_DIR = ROOT / "00_memory" / "user_memories"

class MemoryManager:
    def __init__(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    def _get_user_path(self, user_id: int) -> Path:
        return MEMORY_DIR / f"{user_id}.json"

    def load_memory(self, user_id: int) -> dict:
        """โหลดความจำของผู้ใช้ หากไม่เคยมีให้สร้างโครงสร้างเริ่มต้น"""
        path = self._get_user_path(user_id)
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "user_id": user_id,
            "short_term_buffer": [],
            "long_term_summary": {
                "last_updated": "",
                "project_context": "ไม่มีบริบทก่อนหน้านี้",
                "preferred_tools": [],
                "key_decisions": "",
                "current_status": ""
            }
        }

    def save_memory(self, user_id: int, memory_data: dict):
        """บันทึกข้อมูลลงไฟล์ JSON"""
        path = self._get_user_path(user_id)
        path.write_text(json.dumps(memory_data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_to_short_term(self, user_id: int, role: str, content: str):
        """เก็บประวัติคุยดิบล่าสุด จำกัดไว้ไม่เกิน 5 ข้อความเพื่อไม่ให้ระบบหนัก"""
        memory = self.load_memory(user_id)
        memory["short_term_buffer"].append({"role": role, "content": content})
        # สไลด์เอาเฉพาะ 5 ข้อความล่าสุด (Buffer ซ่อมแซมตัวเอง)
        if len(memory["short_term_buffer"]) > 5:
            memory["short_term_buffer"] = memory["short_term_buffer"][-5:]
        self.save_memory(user_id, memory)

    async def compress_and_update_long_term(self, user_id: int):
        """
        ใช้ LLM ในการบีบอัดข้อความยาวๆ ให้เหลือเฉพาะสรุปสาระสำคัญ (Semantic Recall)
        """
        memory = self.load_memory(user_id)
        if not memory["short_term_buffer"]:
            return

        # ดึงประวัติสั้นมาจัดฟอร์แมตให้ AI อ่าน
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in memory["short_term_buffer"]])
        current_summary = json.dumps(memory["long_term_summary"], ensure_ascii=False)

        prompt = f"""
        คุณคือระบบจัดการความจำระยะยาวของ AI Agent หน้าที่ของคุณคืออัปเดตข้อมูลสรุปของโปรเจกต์ 
        จากบทสนทนาล่าสุดที่เกิดขึ้น เพื่อไม่ให้ระบบต้องจดจำคำพูดไร้สาระทั้งหมด

        ข้อมูลสรุปเดิมในระบบ:
        {current_summary}

        บทสนทนาล่าสุดที่เพิ่งคุยกัน:
        {history_text}

        จงอัปเดตและสรุปข้อมูลใหม่ให้อยู่ในรูปแบบ JSON เท่านั้น ห้ามตอบเป็นคำอธิบายอื่น:
        {{
            "project_context": "สรุปเป้าหมายหรือตัวโปรเจกต์สั้นๆ ในประโยคเดียว",
            "preferred_tools": ["รายชื่อเครื่องมือหรือเทคโนโลยีที่คุยกัน (เก็บเป็น array)"],
            "key_decisions": "การตัดสินใจหลักๆ หรือคำสั่งสำคัญที่ตกลงกันล่าสุด",
            "current_status": "สถานะปัจจุบันของงานหรือสิ่งที่ผู้ใช้กำลังรออยู่"
        }}
        """
        
        try:
            # ใช้ Fast tier ในการสรุปประหยัดและเร็ว
            ai_response = await provider_router.request_llm(prompt, tier="fast")
            cleaned_json = ai_response.replace("```json", "").replace("
```", "").strip()
            new_summary = json.loads(cleaned_json)
            
            new_summary["last_updated"] = dt.datetime.now().isoformat()
            memory["long_term_summary"] = new_summary
            self.save_memory(user_id, memory)
            print(f"🧠 [Memory Manager] Long-term summary compressed for user {user_id}")
        except Exception as e:
            print(f"⚠️ [Memory Error] ไม่สามารถสรุปความจำได้: {e}")

memory_manager = MemoryManager()