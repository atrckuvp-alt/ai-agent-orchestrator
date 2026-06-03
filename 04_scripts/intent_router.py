import json
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
REGISTRY_PATH = ROOT / "00_memory" / "team_registry.json"

class IntentRouter:
    def __init__(self):
        pass

    def _load_registry(self):
        if not REGISTRY_PATH.exists():
            return {"teams": {}}
        try:
            return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ [IntentRouter Error] ไม่สามารถอ่านคลังทะเบียนทีมได้: {e}")
            return {"teams": {}}

    def route_user_intent(self, user_message: str) -> str:
        """
        [LAYER 2 — Intent Routing] วิเคราะห์เจตนาของผู้ใช้
        รองรับการแยกแยะระหว่าง งานเฉพาะทาง (Infra/Team) และ คำทักทายทั่วไป (General Chat)
        """
        message_lower = user_message.lower().strip()
        registry = self._load_registry()
        
        print(f"🧠 [Intent Router] กำลังวิเคราะห์ข้อความ: '{user_message}'")
        
        # 1. ดักจับกลุ่มคำทักทาย คำบอกเล่าทั่วไป หรือถามความสามารถ
        general_keywords = ["สวัสดี", "สวีสดี", "hello", "hi", "ทักทาย", "ทำอะไรได้บ้าง", "ช่วยอะไรได้บ้าง", "เป็นใคร"]
        if any(gk in message_lower for gk in general_keywords):
            print("💬 [Intent Router] ตรวจพบคำทักทาย/สอบถามทั่วไป -> สับสายไปที่ general_chat")
            return "general_chat"
        
        # 2. สแกนหาคำสำคัญ (Keywords Matching) ตามที่ตั้งไว้ในคลังความจำทีม
        for team_key, team_info in registry.get("teams", {}).items():
            keywords = team_info.get("keywords", [])
            if any(kw in message_lower for kw in keywords):
                print(f"🎯 [Intent Router] ตรวจพบการจับคู่โยนงานไปที่ทีม -> {team_key}")
                return team_key
                
        # 3. Heuristic Fallback: ค้นหาคำกริยาเชิงวิจัยหรือการสร้างระบบ
        research_keywords = ["ช่วย", "หา", "วิจัย", "ทำ", "สร้าง", "ระบบ", "scout", "wellness"]
        if any(w in message_lower for w in research_keywords):
            print("⚠️ [Intent Router] ไม่เจอคำเจาะจง แต่บริบทเข้าข่ายงานวิจัย ส่งเข้า default: infrastructure_team")
            return "infrastructure_team"
            
        return "unknown"

intent_router = IntentRouter()