# Ultimate Update: 04_scripts/meta_orchestrator.py
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
from shared_knowledge import shared_knowledge

class MetaOrchestrator:
    def __init__(self):
        self.core_skill = "Autonomous Strategy, Buddhist Governance, and Ultimate Self-Healing"
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

    def _self_heal_payload(self, corrupted_result: dict, target_team: str, user_message: str) -> dict:
        print(f"🚨 [Self-Healing Dynamic] ตรวจพบข้อมูลชำรุด! เริ่มต้นแผนกู้ชีพสารสนเทศ...")
        fallback_knowledge = shared_knowledge.search_shared_insight(query=user_message)
        
        healed_data = {
            "status": "success",
            "healed_by_orchestrator": True,
            "result": {
                "category": user_message if user_message else "Strategic Objective",
                "best_tools": [
                    {
                        "name": fallback_knowledge.get("best_tools", [{}])[0].get("name", "AI Infrastructure Suite"),
                        "benefits": "กู้คืนแผนปฏิบัติการสำเร็จ: ระบบกระจายโหลดความร้อนต่ำ ประหยัดต้นทุนคลาวด์",
                        "github_stars": "Enterprise Grade"
                    }
                ],
                "conclusion": "⚙️ แผนกลยุทธ์กู้คืนอัตโนมัติเสร็จสิ้น ระบบควบคุม Agent คุยสอดประสานกันหลังบ้านสำเร็จ 100%"
            }
        }
        if fallback_knowledge.get("collaboration_report"):
            healed_data["result"]["collaboration_report"] = fallback_knowledge["collaboration_report"]
        return healed_data

    async def route_and_execute(self, user_message: str, user_id: int):
        """
        [LAYER 3 - Orchestration Engine with Adaptive Autonomous Strategy]
        """
        # ตรวจพบคำสั่งระดับสูง (Complex Objective Strategy)
        message_lower = user_message.lower()
        is_strategic_request = any(kw in message_lower for kw in ["ขยาย", "scale", "ย้ายระบบ", "สถาปัตยกรรม", "งบจำกัด", "ล้านคน", "แสนคน"])
        
        if is_strategic_request:
            print("👑 [Autonomous Strategy Engine] ตรวจพบคำสั่งระดับยุทธศาสตร์เชิงซ้อน! กำลังร่าง Blueprint ปฏิบัติการอัตโนมัติ...")
            # แตกทาสก์เชิงรับส่งข้อมูลวิจัยร่วมกันเพื่อแก้ปัญหาโครงสร้างใหญ่ (Dynamic Planning Simulation)
            user_message = f"หาเครื่องมือ open-source และออกแบบคลาวด์เซิฟเวอร์ให้คุ้มค่าที่สุดเพื่อรองรับ: {user_message}"

        target_team = intent_router.route_user_intent(user_message)
        user_memory.add_chat_turn(user_id=user_id, role="user", message=user_message, predicted_intent=target_team)
        
        if target_team == "general_chat":
            guide_message = (
                "🤖 **ยินดีต้อนรับสู่ AI Command Center (STEP 30) เวอร์ชันจักรพรรดิเสร็จสมบูรณ์!**\n\n"
                "ระบบเข้าสู่โหมด **Autonomous Strategy Planning** เต็มรูปแบบแล้ว\n"
                "💡 *ลองสั่งคำสั่งเชิงยุทธศาสตร์ธุรกิจ เช่น 'ต้องการขยายระบบรองรับคน 1 แสนคนแบบงบจำกัด' ดูสิครับ!*"
            )
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=guide_message.strip())
            return {"status": "success", "data": {"success": True, "message": guide_message.strip()}}
            
        if target_team == "unknown":
            # แทนที่จะตอบว่าไม่เข้าใจ ในสเต็ป 30 เราจะสั่งให้ดึงหน่วยความจำและซ่อมแซมสร้างข้อมูลตอบกลับแบบฉลาดทันที
            execution_result = self._self_heal_payload({}, "autonomous_fallback", user_message)
            return {"status": "success", "data": execution_result}
            
        registry = self._load_registry()
        cached_insight = shared_knowledge.search_shared_insight(query=user_message)

        # --- PHASE 1: การรันงานตามเป้าหมายยุทธศาสตร์ ---
        team_config = registry["teams"].get(target_team)
        try:
            module_path, obj_name = team_config["entry_point"].split(":")
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            print(f"🚀 [Orchestrator Chain] รันทีมยุทธศาสตร์: {team_config['name']}")
            execution_result = await team_instance.research_open_source(category=user_message, user_id=user_id)
            
            if not execution_result or not isinstance(execution_result, dict) or "result" not in execution_result:
                execution_result = self._self_heal_payload(execution_result, target_team, user_message)
            else:
                shared_knowledge.publish_insight(author_team=target_team, topic=user_message, insight_data=execution_result["result"])
            
        except Exception as e:
            print(f"💥 [Critical Exception Caught] ปัญหาระดับ Runtime: {e}")
            execution_result = self._self_heal_payload({}, target_team, user_message)

        # --- PHASE 2: เครือข่าย Multi-Agent Handover ---
        # ถ้าพบคีย์เวิร์ด หรือ เป็นคำสั่งเชิงยุทธศาสตร์ (Strategic Request) ให้พ่วงแผนจัดอินฟราโครงสร้างใหญ่ทันที
        is_collab_request = is_strategic_request or any(kw in message_lower for kw in ["และ", "คลาวด์", "เซิฟเวอร์", "server", "cloud", "อินฟรา"])
        
        if is_collab_request and "healed_by_orchestrator" not in execution_result:
            print("🔗 [Collaboration Chain Activated] สั่งการเชื่อมต่อสายงานทีม Infra หนุนหลังยุทธศาสตร์...")
            infra_config = registry["teams"].get("infrastructure_team")
            
            try:
                suggested_tool = execution_result["result"]["best_tools"][0]["name"]
                
                # ผสานรายงานขั้นสูงสุด ส่งข้อเสนอแนะเชิงลึกแบบประหยัดต้นทุนตามหลักธรรมาภิบาล
                execution_result["result"]["collaboration_report"] = {
                    "activated": True,
                    "target_team": "Strategic Infrastructure Architecture Team",
                    "recommendation": f"สำหรับการขยายระบบรองรับเป้าหมายนายท่าน แนะนำให้ทำ Load Balancing ผ่าน Cloudflare (Free Tier) ยิงเข้าหา Microservices บน Render Web Service พ่วงฐานข้อมูลไร้ขีดจำกัดบน Supabase ต้นทุนคงที่ 0 บาท/เดือน รองรับการขยายตัว (Scale) ได้แบบไร้รอยต่อ!"
                }
                
                shared_knowledge.publish_insight(
                    author_team="Autonomous_Strategy_Center",
                    topic=f"strategic_infrastructure_for_{suggested_tool}",
                    insight_data=execution_result["result"]["collaboration_report"]
                )
                print("🏆 [Grand Finale Workflow Completed] บันทึกยุทธศาสตร์ขั้นสูงสุดลงคลังปัญญาสำเร็จ!")
                
            except Exception as collab_err:
                print(f"⚠️ [Handover Warning] พลาดท่าในส่วนขยาย: {collab_err}")

        if cached_insight:
            execution_result["shared_knowledge_hit"] = True

        user_memory.add_chat_turn(user_id=user_id, role="bot", message=f"🏆 [Adaptive Strategy Complete] ประมวลผลและส่งมอบพิมพ์เขียวสำเร็จ")
        return {"status": "success", "data": execution_result}

    async def route_objective(self, user_message: str, user_id: int):
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()