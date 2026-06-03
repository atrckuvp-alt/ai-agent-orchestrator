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
        [LAYER 2 — Intent Routing with Multi-Team Routing]
        คัดแยกเจตนาว่าข้อความต้องการใช้ทีมโครงสร้างพื้นฐาน (Infra) หรือทีมโอเพนซอร์สซอฟต์แวร์ (OSS)
        """
        message_lower = user_message.lower().strip()
        registry = self._load_registry()
        
        print(f"🧠 [Intent Router] กำลังวิเคราะห์ข้อความเจาะจงเป้าหมาย: '{user_message}'")
        
        # 1. คัดกรองคำทักทายสนทนาทั่วไป
        general_keywords = ["สวัสดี", "สวีสดี", "hello", "hi", "ทักทาย", "ทำอะไรได้บ้าง", "ช่วยอะไรได้บ้าง", "เป็นใคร"]
        if any(gk in message_lower for gk in general_keywords):
            return "general_chat"
        
        # 2. ค้นหาแบบ Keyword Match ตรงจากฐานทะเบียนทีมย่อย (Dynamic Search)
        for team_key, team_info in registry.get("teams", {}).items():
            keywords = team_info.get("keywords", [])
            if any(kw in message_lower for kw in keywords):
                print(f"🎯 [Intent Router] ตรวจพบคำเฉพาะเจาะจง! โยนงานเข้าทีม -> {team_key}")
                return team_key
                
        # 3. Fallback Heuristics แยกแยะประเภทกรณีไม่มีคีย์เวิร์ดตรงตัว
        # แนวการจัดการระบบ / คลาวด์ / เซิฟเวอร์ / เช็คระบบ -> infrastructure_team
        infra_clues = ["ฐานข้อมูล", "เซิฟเวอร์", "db", "cloud", "server", "deploy", "optimize", "ระบบ"]
        if any(ic in message_lower for ic in infra_clues):
            print("💡 [Intent Router Fallback] ตรวจพบเบาะแสเชิงระบบ -> ส่งเข้า infrastructure_team")
            return "infrastructure_team"

        # แนวการหาเครื่องมือใช้งาน / ซอฟต์แวร์สำเร็จรูป / มาร์เก็ตติ้ง -> oss_research_team
        oss_clues = ["หา", "scout", "marketing", "โอเพนซอร์ส", "ซอฟต์แวร์", "แอป", "คู่แข่ง", "automation", "tool"]
        if any(oc in message_lower for oc in oss_clues):
            print("💡 [Intent Router Fallback] ตรวจพบเบาะแสเชิงซอฟต์แวร์ใช้งาน -> ส่งเข้า oss_research_team")
            return "oss_research_team"
            
        return "unknown"

intent_router = IntentRouter()