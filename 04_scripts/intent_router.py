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
        [LAYER 2 — Intent Routing with Multi-Team Priority]
        """
        message_lower = user_message.lower().strip()
        
        print(f"🧠 [Intent Router] กำลังวิเคราะห์ข้อความเจาะจงเป้าหมาย: '{user_message}'")
        
        # 1. คัดกรองคำทักทายสนทนาทั่วไป
        general_keywords = ["สวัสดี", "สวีสดี", "hello", "hi", "ทักทาย", "ทำอะไรได้บ้าง", "ช่วยอะไรได้บ้าง", "เป็นใคร"]
        if any(gk in message_lower for gk in general_keywords):
            return "general_chat"
        
        # 2. [CRITICAL BUGFIX] ดักจับคำสั่งคอมโบควบสองทีม (Collaboration Pattern Detection)
        # ถ้าพบบทสนทนาที่มีคีย์เวิร์ดของทั้งสองสายงานในที่เดียวกัน ให้ส่งเข้า OSS Team เสมอ เพื่อไปเริ่ม Workflow Chain
        has_infra_clue = any(ic in message_lower for ic in ["infra", "cloud", "database", "เซิฟเวอร์", "เซอเวอ", "คลาวด์", "ระบบ"])
        has_oss_clue = any(oc in message_lower for oc in ["oss", "open-source", "หาซอฟต์แวร์", "เครื่องมือ", "crm", "automation", "tool"])
        
        if has_infra_clue and has_oss_clue:
            print("🎯 [Intent Router Combo] ตรวจพบคำสั่งควบคู่! จัดลำดับความสำคัญส่งเข้า -> oss_research_team เพื่อเริ่มกระบวนการส่งไม้ต่อ")
            return "oss_research_team"

        # 3. Fallback Heuristics แยกทีมเดี่ยวๆ (กรณีพิมพ์สั่งอย่างใดอย่างหนึ่ง)
        if has_oss_clue:
            return "oss_research_team"
            
        if has_infra_clue:
            return "infrastructure_team"
            
        return "unknown"

intent_router = IntentRouter()