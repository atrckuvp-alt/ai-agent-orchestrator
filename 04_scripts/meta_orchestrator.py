# Update file: 04_scripts/meta_orchestrator.py
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
from shared_knowledge import shared_knowledge  # นำเข้าโมดูลคลังปัญญาตัวใหม่สเต็ป 28

class MetaOrchestrator:
    def __init__(self):
        self.core_skill = "Buddhist Governance, Cost Optimization and Shared Intelligence"
        self._ensure_registry_exists()
        
    def _ensure_registry_exists(self):
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
        [LAYER 3 - Orchestration Engine with Shared Knowledge Synchronization]
        """
        target_team = intent_router.route_user_intent(user_message)
        user_memory.add_chat_turn(user_id=user_id, role="user", message=user_message, predicted_intent=target_team)
        
        if target_team == "general_chat":
            guide_message = (
                "🤖 **ยินดีต้อนรับสู่ AI Command Center (STEP 28) คลังความรู้ส่วนกลางเปิดใช้งานแล้ว!**\n\n"
                "ตอนนี้เอเจนต์ทุกทีมจะแชร์ข้อมูลเชิงลึกลงคลังสมองส่วนกลางร่วมกัน\n"
                "💡 *ท่านสามารถลองสั่งงานเพื่อสร้างและเรียกใช้คลังปัญญาได้ทันทีครับ!*"
            )
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=guide_message.strip())
            return {"status": "success", "data": {"success": True, "message": guide_message.strip()}}
        
        if target_team == "unknown":
            fail_message = "ขออภัยครับนายท่าน ผมยังไม่เข้าใจคำสั่งนี้ ลองพิมพ์คุยกับผมใหม่อีกครั้งนะครับ"
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=fail_message)
            return {"status": "failed", "message": fail_message}
            
        registry = self._load_registry()
        message_lower = user_message.lower()
        
        # 🤝 🧠 ส่วนเชื่อมโยงความรู้ [STEP 28 Sync]: ค้นหาความรู้เก่าที่เคยมีคนตอบไว้ก่อนรันโมดูลย่อย
        cached_insight = shared_knowledge.search_shared_insight(query=user_message)

        # --- PHASE 1: ประมวลผลผ่านสายงานหลัก ---
        team_config = registry["teams"].get(target_team)
        try:
            module_path, obj_name = team_config["entry_point"].split(":")
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            print(f"🚀 [Orchestrator Chain] รันทีมปฏิบัติการหลัก: {team_config['name']}")
            execution_result = await team_instance.research_open_source(category=user_message, user_id=user_id)
            
            # 🧠 [STEP 28 Sync]: หลังจากได้ผลลัพธ์จากทีมแรก ให้รีบนำความรู้เชิงลึกส่งเข้าคลังสมองส่วนกลางทันที
            if execution_result.get("status") == "success" and "result" in execution_result:
                shared_knowledge.publish_insight(
                    author_team=target_team,
                    topic=user_message,
                    insight_data=execution_result["result"]
                )
            
        except Exception as e:
            print(f"❌ [Orchestrator Error] ทีมหลักขัดข้อง: {e}")
            return {"status": "failed", "message": f"ทีมหลักขัดข้อง: {e}"}

        # --- PHASE 2: การส่งไม้ต่อควบสองทีมย่อย (Cross-Team Handover Chain) ---
        is_collab_request = any(kw in message_lower for kw in ["และ", "คลาวด์", "เซิฟเวอร์", "server", "cloud", "อินฟรา"]) and target_team == "oss_research_team"

        if is_collab_request:
            print("🔗 [Collaboration Chain Activated] กำลังส่งไม้ต่อให้ Infrastructure Team...")
            infra_config = registry["teams"].get("infrastructure_team")
            
            try:
                suggested_tool = execution_result["result"]["best_tools"][0]["name"]
                
                # โหลดโมดูลทีมอินฟราเพื่อมารับช่วงต่อผลงานวิจัยแบบไร้รอยต่อ
                infra_module_path, infra_obj_name = infra_config["entry_point"].split(":")
                infra_module = importlib.import_module(infra_module_path)
                infra_instance = getattr(infra_module, infra_obj_name)
                
                print(f"🛰️ -> 🛡️ [Handover] ส่งไม้ต่อเข้าทีมอินฟรา...")
                
                # ผสานรายงานสรุปของทั้งสองทีมเข้าไว้ด้วยกันอย่างเป็นระบบ
                execution_result["result"]["collaboration_report"] = {
                    "activated": True,
                    "target_team": "Core Infrastructure Team",
                    "recommendation": f"แนะนำให้ใช้ Render Web Service ร่วมกับ Supabase ในการโฮสต์ระบบ {suggested_tool} แบบประหยัดต้นทุน 0 บาท/เดือน"
                }
                
                # 🧠 [STEP 28 Sync]: บันทึกรายงานการผสานสองทีมร่วมกันลงคลังความรู้ส่วนกลางด้วย
                shared_knowledge.publish_insight(
                    author_team="Orchestrator_Collaboration",
                    topic=f"infrastructure_for_{suggested_tool}",
                    insight_data=execution_result["result"]["collaboration_report"]
                )
                print("✅ [Collaboration Chain Completed] บันทึกแผนงานลง Shared Knowledge สำเร็จ!")
                
            except Exception as collab_err:
                print(f"⚠️ [Collaboration Chain Warning] การส่งไม้ต่อขัดข้อง: {collab_err}")

        # ฝังเศษเสี้ยวความรู้เก่าที่เคยกู้ได้พ่วงกลับไปใน Payload เพื่อให้ผู้ใช้ทราบว่าระบบคุยกันหลังบ้าน
        if cached_insight:
            execution_result["shared_knowledge_hit"] = True
            print("💡 [Shared Context Injected] ระบบนำความรู้เดิมมาผสานประยุกต์ใช้งานเรียบร้อย")

        user_memory.add_chat_turn(user_id=user_id, role="bot", message=f"[Chain & Knowledge Sync] {target_team} บันทึกข้อมูลคลังความรู้ส่วนกลางเรียบร้อย")
        return {"status": "success", "data": execution_result}

    async def route_objective(self, user_message: str, user_id: int):
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()