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
from user_memory import user_memory

class MetaOrchestrator:
    def __init__(self):
        self.core_skill = "Buddhist Governance and Cost Optimization"
        self._ensure_registry_exists()
        
    def _ensure_registry_exists(self):
        """
        [STEP 25 - Team Registry Expansion]
        ลงทะเบียนทีมปฏิบัติการทั้งหมดที่มีอยู่จริงในโฟลเดอร์เข้าสู่คลังทะเบียนกลาง
        """
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        default_registry = {
            "teams": {
                "infrastructure_team": {
                    "name": "Core Infrastructure & Cloud DevOps Team",
                    "description": "วิจัย ออกแบบ และแนะนำระบบคลาวด์ ฐานข้อมูล และเครื่องมือสถาปัตยกรรมระดับเซิฟเวอร์แบบประหยัด",
                    "keywords": ["infra", "cloud", "database", "sqlite", "postgres", "supabase", "optimize", "เซิฟเวอร์", "คลาวด์", "เช็คระบบ"],
                    "entry_point": "teams.infrastructure_team.infrastructure_team:infrastructure_team"
                },
                "oss_research_team": {
                    "name": "Open-Source Scouting & Research Team",
                    "description": "สำรวจ ค้นหา และเปรียบเทียบซอฟต์แวร์เครื่องมือ Open-Source สำหรับธุรกิจและการตลาด",
                    "keywords": ["oss", "open-source", "marketing", "automation", "tool", "github", "scout", "scouting", "เครื่องมือ", "คู่แข่ง", "หาซอฟต์แวร์"],
                    "entry_point": "teams.oss_research_team.oss_research_team:oss_research_team"
                }
            }
        }
        
        REGISTRY_PATH.write_text(json.dumps(default_registry, indent=2, ensure_ascii=False), encoding="utf-8")
        print("📁 [Team Registry] ขยายและลงทะเบียนระบบทีมคู่ขนานเรียบร้อย!")

    def _load_registry(self):
        try:
            return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"teams": {}}

    async def route_and_execute(self, user_message: str, user_id: int):
        """
        [LAYER 3 - Orchestration Engine with Dynamic Injection]
        """
        # 1. ส่งข้อความวิเคราะห์เจตนา (Intent Routing)
        target_team = intent_router.route_user_intent(user_message)
        
        # 2. บันทึกความจำขาเข้าลงคลังระยะยาว (Conversational Memory)
        user_memory.add_chat_turn(user_id=user_id, role="user", message=user_message, predicted_intent=target_team)
        
        # 3. จัดการกรณีข้อความพูดคุยทั่วไป
        if target_team == "general_chat":
            guide_message = """
🤖 **สวัสดีครับนายท่าน! ผมคือ AI Command Center ของท่าน** ขณะนี้ระบบเปิดใช้งาน **STEP 25 (Multi-Team Routing)** พร้อมรับคำสั่งแยกสายปฏิบัติการจริงแล้วครับ!

💡 **ท่านสามารถสั่งงานเรียกใช้ทีมย่อยได้ตามหัวข้อเหล่านี้:**
🛡️ *ทีมสถาปัตยกรรมอินฟรา (Infrastructure Team):*
• *"ช่วยวิจัยฐานข้อมูลแบบฟรีให้หน่อย"*
• *"หาตัวเลือกคลาวด์เซิฟเวอร์ประหยัดต้นทุน"*

🛰️ *ทีมจัดหาซอฟต์แวร์ (Open-Source Scouting Team):*
• *"ไปหา open-source marketing automation ดีๆ หน่อย"*
• *"ช่วยสเกาต์หาเครื่องมือทำเว็บบอร์ดโอเพนซอร์ส"*
            """
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=guide_message.strip())
            return {"status": "success", "data": {"success": True, "message": guide_message.strip()}}
        
        if target_team == "unknown":
            fail_message = "ขออภัยครับนายท่าน ผมยังไม่เข้าใจคำสั่งนี้ ลองพิมพ์เกี่ยวกับ 'วิจัยระบบอินฟราคลาวด์' หรือ 'หาโอเพนซอร์สมาร์เก็ตติ้ง' ดูไหมครับ?"
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=fail_message)
            return {"status": "failed", "message": fail_message}
            
        # 4. โหลดคอนฟิกทีมย่อยแบบ Dynamic Module Loading
        registry = self._load_registry()
        team_config = registry["teams"].get(target_team)
        
        if not team_config:
            return {"status": "failed", "message": f"ไม่พบข้อมูลโมดูลของทีม {target_team} ในความจำ"}
            
        try:
            entry_point_str = team_config["entry_point"]
            module_path, obj_name = entry_point_str.split(":")
            
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            print(f"🚀 [Orchestrator] กำลังส่งไม้ต่อให้ทีม: {team_config['name']}...")
            result = await team_instance.research_open_source(category=user_message, user_id=user_id)
            
            # บันทึกสถานะบอทหลังปฏิบัติการสำเร็จ
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=f"[System Executed] {team_config['name']} ประมวลผลและส่งรายงานเรียบร้อย")
            return {"status": "success", "data": result}
            
        except Exception as e:
            print(f"❌ [Orchestrator Failover Alert] โหลดหรือรันโมดูลทีมย่อยล้มเหลว: {e}")
            return {
                "status": "fallback_activated",
                "message": f"ระบบทีมปฏิบัติการขัดข้องชั่วคราว แต่หน่วยความจำหลักปลอดภัยดีครับ (Error: {e})"
            }

    async def route_objective(self, user_message: str, user_id: int):
        print(f"🔄 [Orchestrator Alias] สับสายฟังก์ชันจาก route_objective -> route_and_execute")
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()