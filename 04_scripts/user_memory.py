import json
from pathlib import Path
import datetime as dt

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
MEMORY_DIR = ROOT / "00_memory" / "user_memories"

class UserMemory:
    def __init__(self):
        # ตรวจสอบและสร้างโฟลเดอร์เก็บความจำรายผู้ใช้หากยังไม่มี
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    def _get_user_file_path(self, user_id: int) -> Path:
        return MEMORY_DIR / f"user_{user_id}.json"

    def load_memory(self, user_id: int) -> dict:
        """โหลดประวัติการคุยและบริบทล่าสุดของผู้ใช้จาก 00_memory"""
        file_path = self._get_user_file_path(user_id)
        if not file_path.exists():
            return {
                "user_id": user_id,
                "last_interaction": None,
                "current_context": {},
                "chat_history": []
            }
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ [UserMemory Error] อ่านไฟล์ความจำผู้ใช้ {user_id} ล้มเหลว: {e}")
            return {"user_id": user_id, "last_interaction": None, "current_context": {}, "chat_history": []}

    def save_memory(self, user_id: int, memory_data: dict):
        """บันทึกข้อมูลความจำผู้ใช้ลงดิสก์"""
        file_path = self._get_user_file_path(user_id)
        try:
            file_path.write_text(json.dumps(memory_data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"❌ [UserMemory Error] บันทึกไฟล์ความจำผู้ใช้ {user_id} ล้มเหลว: {e}")

    def add_chat_turn(self, user_id: int, role: str, message: str, predicted_intent: str = None):
        """บันทึกไดอะล็อกการสนทนาล่าสุดลงในคลังความจำ และจำกัดความยาวเพื่อประหยัดสเปซ"""
        memory = self.load_memory(user_id)
        
        # เพิ่มเทิร์นการคุย
        turn_entry = {
            "timestamp": dt.datetime.now().isoformat(),
            "role": role,
            "message": message
        }
        if predicted_intent:
            turn_entry["intent"] = predicted_intent
            # เก็บเจตนาล่าสุดไว้ใน context ปัจจุบันด้วย เพื่อให้ระบบรู้ว่าคุยเรื่องอะไรค้างไว้
            memory["current_context"]["last_intent"] = predicted_intent

        memory["chat_history"].append(turn_entry)
        memory["last_interaction"] = dt.datetime.now().isoformat()

        # [Cost Optimization] จำกัดประวัติเก็บไว้เฉพาะ 10 เทิร์นล่าสุด เพื่อไม่ให้ไฟล์บวมและกินเน็ตฟรีคลาวด์
        if len(memory["chat_history"]) > 20:
            memory["chat_history"] = memory["chat_history"][-20:]

        self.save_memory(user_id, memory)
        print(f"💾 [UserMemory Log] บันทึกประวัติการคุยของ {user_id} เรียบร้อย (Role: {role})")

    def get_last_intent(self, user_id: int) -> str:
        """ช่วยดึงบริบทว่าประโยคก่อนหน้านี้ผู้ใช้คุยเรื่องอะไรไว้"""
        memory = self.load_memory(user_id)
        return memory.get("current_context", {}).get("last_intent", "unknown")

user_memory = UserMemory()