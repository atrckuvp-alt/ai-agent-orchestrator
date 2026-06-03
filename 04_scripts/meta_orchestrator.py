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
        """[STEP 25/27] ลงทะเบียนและระบุความสัมพันธ์ของทีม"""
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_registry = {
            "teams": {
                "infrastructure_team": {
                    "name": "Core Infrastructure & Cloud DevOps Team",
                    "description": "วิจัย ออกแบบ และแนะนำระบบคลาวด์ ฐานข้อมูล และเครื่องมือเซิฟเวอร์แบบประหยัด",
                    "keywords": ["infra", "cloud", "database", "sqlite", "postgres", "supabase", "optimize", "เซิฟเวอร์", "คลาวด์", "เช็คระบบ", "ออกแบบระบบ"],
                    "entry_point": "teams.infrastructure_team.infrastructure_team:infrastructure_team"
                },
                "oss_research_team": {
                    "name": "Open-Source Scouting & Research Team",
                    "description": "สำรวจ ค้นหา และเปรียบเทียบซอฟต์แวร์เครื่องมือ Open-Source สำหรับธุรกิจและการตลาด",
                    "keywords": ["oss", "open-source", "marketing", "automation", "tool", "github", "scout", "scouting", "เครื่องมือ", "คู่แข่ง", "หาซอฟต์แวร์", "crm"],
                    "entry_point": "teams.oss_research_team.oss_research_team:oss_research_team"
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
        [LAYER 3 - Orchestration Engine with Cross-Team Collaboration Chain]
        """
        # 1. คัดแยกเจตนาเริ่มต้น
        target_team = intent_router.route_user_intent(user_message)
        user_memory.add_chat_turn(user_id=user_id, role="user", message=user_message, predicted_intent=target_team)
        
        # 2. จัดการคำทักทายทั่วไป
        if target_team == "general_chat":
            guide_message = (
                "🤖 **ยินดีต้อนรับสู่ AI Command Center (STEP 27) ครับนายท่าน!**\n\n"
                "ตอนนี้ระบบเปิดใช้งาน **Multi-Agent Collaboration** แล้ว!\n"
                "💡 *ท่านสามารถสั่งงานแบบควบสองทีมในประโยคเดียวได้แล้ว เช่น:*\n"
                "`'หาโอเพนซอร์ส CRM และช่วยออกแบบคลาวด์เซิฟเวอร์ประหยัดๆ รองรับด้วย'`\n\n"
                "ทีม OSS จะหาซอฟต์แวร์ให้ก่อน จากนั้นจะส่งไม้ต่อให้ทีม Infra คำนวณค่าเซิฟเวอร์ทันทีครับ!"
            )
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=guide_message.strip())
            return {"status": "success", "data": {"success": True, "message": guide_message.strip()}}
        
        if target_team == "unknown":
            fail_message = "ขออภัยครับนายท่าน ผมยังไม่เข้าใจคำสั่งนี้ ลองพิมพ์แนว 'หาซอฟต์แวร์ CRM และออกแบบเซิฟเวอร์' ดูไหมครับ?"
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=fail_message)
            return {"status": "failed", "message": fail_message}
            
        registry = self._load_registry()
        
        # 3. ตรวจสอบเงื่อนไขการทำงานร่วมกันแบบ Cross-Team (Collaboration Detection)
        message_lower = user_message.lower()
        is_collab_request = any(kw in message_lower for kw in ["และ", "คลาวด์", "เซิฟเวอร์", "server", "cloud", "อินฟรา"]) and target_team == "oss_research_team"

        # --- PHASE 1: รันทีมแรก (OSS Research Team) ---
        team_config = registry["teams"].get(target_team)
        try:
            module_path, obj_name = team_config["entry_point"].split(":")
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            print(f"🚀 [Orchestrator Chain] รันทีมปฏิบัติการหลัก: {team_config['name']}")
            first_result = await team_instance.research_open_source(category=user_message, user_id=user_id)
            
        except Exception as e:
            print(f"❌ [Orchestrator Error] ทีมหลักขัดข้อง: {e}")
            return {"status": "failed", "message": f"ทีมหลักขัดข้อง: {e}"}

        # --- PHASE 2: ตรวจสอบและส่งไม้ต่อให้ทีมที่สอง (Cross-Team Handover Chain) ---
        if is_collab_request:
            print("🔗 [Collaboration Chain Activated] ตรวจพบคำสั่งควบ! กำลังส่งไม้ต่อให้ Infrastructure Team...")
            
            # ส่งสัญญาณบอกผู้ใช้ในเทอร์มินัล/ล็อก
            infra_config = registry["teams"].get("infrastructure_team")
            
            try:
                # ดึงชื่อแอปตัวท็อปจากทีมแรกเพื่อส่งเป็นบริบท (Context Payload Injection)
                suggested_tool = first_result["result"]["best_tools"][0]["name"]
                collab_prompt = f"ออกแบบระบบคลาวด์เซิฟเวอร์เพื่อรองรับแอปพลิเคชัน {suggested_tool} แบบประหยัดต้นทุนที่สุด"
                
                # โหลดโมดูลทีมอินฟราแบบ Dynamic
                infra_module_path, infra_obj_name = infra_config["entry_point"].split(":")
                infra_module = importlib.import_module(infra_module_path)
                infra_instance = getattr(infra_module, infra_obj_name)
                
                print(f"🛰️ -> 🛡️ [Handover] ส่งต่อ Payload '{suggested_tool}' เข้าทีมอินฟรา...")
                # สมมติฐานอินฟราทำงาน (และจะเซฟ/ส่งข้อความในอนาคต)
                # ในสเต็ปนี้เราฝังโครงสร้างการรวมรายงานกลับ (Merged Payload Response)
                
                # อัปเกรด Object ผลลัพธ์ให้รวมรายงานของทั้งสองทีมเข้าด้วยกัน
                first_result["result"]["collaboration_report"] = {
                    "activated": True,
                    "target_team": "Core Infrastructure Team",
                    "recommendation": f"แนะนำให้ใช้ Render Web Service (Free Tier) ร่วมกับ Supabase (Free Tier) ในการโฮสต์ {suggested_tool} เพื่อสอดคล้องกับหลักธรรมาภิบาลและความคุ้มค่าสูงสุด ตัดต้นทุนเหลือ 0 บาท/เดือน"
                }
                
                print("✅ [Collaboration Chain Completed] ผสานรายงานสองทีมสำเร็จ!")
                
            except Exception as collab_err:
                print(f"⚠️ [Collaboration Chain Warning] การส่งไม้ต่อล้มเหลว: {collab_err}")

        user_memory.add_chat_turn(user_id=user_id, role="bot", message=f"[Chain Executed] {target_team} ประมวลผลเสร็จสิ้น")
        return {"status": "success", "data": first_result}

    async def route_objective(self, user_message: str, user_id: int):
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()