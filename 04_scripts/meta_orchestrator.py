import json
from pathlib import Path
import importlib
import sys

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
REGISTRY_PATH = ROOT / "00_memory" / "team_registry.json"

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from intent_router import intent_router

class MetaOrchestrator:
    def __init__(self):
        self.core_skill = "Buddhist Governance and Cost Optimization"
        self._ensure_registry_exists()
        
    def _ensure_registry_exists(self):
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not REGISTRY_PATH.exists():
            default_registry = {
                "teams": {
                    "infrastructure_team": {
                        "name": "Core Infrastructure Team",
                        "description": "วิจัย ออกแบบ และแนะนำระบบคลาวด์ ฐานข้อมูล และเครื่องมือ Open-Source แบบประหยัดต้นทุน",
                        "keywords": ["infra", "cloud", "database", "open-source", "sqlite", "postgres", "supabase", "optimize", "เซิฟเวอร์"],
                        "entry_point": "teams.infrastructure_team.infrastructure_team:infrastructure_team"
                    }
                }
            }
            REGISTRY_PATH.write_text(json.dumps(default_registry, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_registry(self):
        try:
            return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"teams": {}}

    async def route_and_execute(self, user_message: str, user_id: int):
        """
        [LAYER 3 - Orchestration Engine]
        """
        # 1. ส่งข้อความไปให้สมองส่วนคัดแยกเจตนาทำงาน
        target_team = intent_router.route_user_intent(user_message)
        
        # [NEW LOGIC] รองรับคำทักทายทั่วไป ไม่ปัดคำสั่งทิ้งดื้อๆ
        if target_team == "general_chat":
            guide_message = """
🤖 **สวัสดีครับนายท่าน! ผมคือ AI Command Center ของท่าน** ขณะนี้ระบบกำลังพัฒนาและอยู่ใน **STEP 23 (Intent Router)** ผมสามารถรับคำสั่งภาษาธรรมชาติเพื่อเรียกใช้ทีมปฏิบัติการได้แล้วครับ!

💡 **ท่านสามารถสั่งงานผมในหัวข้อเหล่านี้ได้เลย:**
• *"ช่วยวิจัยฐานข้อมูลแบบฟรีให้หน่อย"*
• *"หาตัวเลือกคลาวด์เซิฟเวอร์ประหยัดต้นทุน"*
• *"ช่วยวางโครงสร้างระบบโปรเจกต์ใหม่"*

_พิมพ์รายละเอียดงานที่ต้องการวิจัยส่งเข้ามาได้เลยครับ ทีมปฏิบัติการย่อยพร้อมสแตนด์บายทำงานให้ท่านทันที!_
            """
            return {"status": "success", "data": {"success": True, "message": guide_message.strip()}}
        
        if target_team == "unknown":
            return {
                "status": "failed",
                "message": "ขออภัยครับนายท่าน ผมยังไม่เข้าใจคำสั่งนี้ หรือยังไม่มีทีมที่รองรับงานประเภทนี้ในระบบครับ ลองพิมพ์ทดสอบเกี่ยวกับ 'วิจัยระบบอินฟราคลาวด์' ดูไหมครับ?"
            }
            
        # 2. รันทีมปฏิบัติการตามปกติ
        registry = self._load_registry()
        team_config = registry["teams"].get(target_team)
        
        if not team_config:
            return {"status": "failed", "message": f"ไม่พบข้อมูลโมดูลของทีม {target_team} ในความจำ"}
            
        try:
            entry_point_str = team_config["entry_point"]
            module_path, obj_name = entry_point_str.split(":")
            
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            print(f"🚀 [Orchestrator] กำลังส่งไม้ต่อให้: {team_config['name']}...")
            result = await team_instance.research_open_source(category=user_message, user_id=user_id)
            return {"status": "success", "data": result}
            
        except Exception as e:
            print(f"❌ [Orchestrator Failover Alert] โหลดโมดูลล้มเหลว: {e}")
            return {
                "status": "fallback_activated",
                "message": f"ระบบทีมปฏิบัติการขัดข้องชั่วคราว แต่หน่วยความจำหลักปลอดภัยดีครับ (Error: {e})"
            }

    async def route_objective(self, user_message: str, user_id: int):
        print(f"🔄 [Orchestrator Alias] สับสายฟังก์ชันจาก route_objective -> route_and_execute")
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()