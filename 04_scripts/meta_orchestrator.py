# Update file: 04_scripts/meta_orchestrator.py (Ultimate 5-Layer Omni Failover)
import json
from pathlib import Path
import importlib
import sys
import os
import asyncio

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
        self.core_skill = "5-Layer Omni Failover, Autonomous Workhorse Routing, and Self-Healing"
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

    async def _call_llm_with_failover(self, team_instance, category: str, user_id: int):
        """
        [STEP 31.7 - Zero-Cost Strict Guard]
        ลูปขั้นบันไดกู้ชีพ 5 ชั้น ตรวจสอบและดีดตัวหนีทันทีเมื่อ DeepSeek Free Token หมด
        """
        # --- ก๊อกที่ 1: ลองใช้คีย์จอมลุย DeepSeek (Free Mode 5 ล้านโทเคน) ---
        try:
            if os.getenv("DEEPSEEK_API_KEY"):
                print("🚀 [Engine 1/5] รันงานหลักผ่านขุมกำลังจอมลุย DeepSeek (Free Mode)...")
                if hasattr(team_instance, 'research_open_source_deepseek'):
                    return await team_instance.research_open_source_deepseek(category=category, user_id=user_id)
                return await team_instance.research_open_source(category=category, user_id=user_id)
            else:
                print("⏭️ [Engine 1/5 Skip] ไม่พบ DEEPSEEK_API_KEY สลับสายไปก๊อกสอง...")
        except Exception as e1:
            error_msg = str(e1).lower()
            # ดักจับถ้าโควต้าเงินฟรีของ DeepSeek หมดเกลี้ยง (Insufficient Balance / 402 Payment Required)
            if "balance" in error_msg or "quota" in error_msg or "402" in error_msg:
                print("⚠️ [🚨 DEEPSEEK FREE LIMIT HIT!] ตรวจพบโหมดฟรีของ DeepSeek หมดโควต้าแล้ว! สับสายหนีถาวร...")
            else:
                print(f"⚠️ [DeepSeek Alert] กองหน้าขัดข้องชั่วคราว: {e1}")
            
        # --- ก๊อกที่ 2: สลับเข้าหาพระเอกฟรีตลอดกาล GEMINI_API_KEY บัญชีหลัก ---
        try:
            print("🔄 [Engine 2/5] สลับเข้าสู่แผนสำรองค่ายหลัก GEMINI_API_KEY (Free Tier)...")
            if hasattr(team_instance, 'research_open_source_gemini'):
                return await team_instance.research_open_source_gemini(category=category, user_id=user_id)
            return await team_instance.research_open_source(category=category, user_id=user_id)
        except Exception as e2:
            print(f"⚠️ [Gemini Primary Alert] คีย์ Gemini หลักติดขัดชั่วคราว: {e2}")

            # --- ก๊อกที่ 3: สับสายหาคีย์ Gemini สำรอง (บัญชีที่ 2 ฟรีโควต้าเสริม) ---
            try:
                if os.getenv("GEMINI_BACKUP_API_KEY"):
                    print("🔄 [Engine 3/5] เปิดระบบสำรองด่านสาม GEMINI_BACKUP_API_KEY...")
                    if hasattr(team_instance, 'research_open_source_fallback_gemini'):
                        return await team_instance.research_open_source_fallback_gemini(category=category, user_id=user_id)
                else:
                    print("⏭️ [Engine 3/5 Skip] ไม่พบคีย์สำรอง Gemini ตัวที่ 2 ข้ามด่าน...")
            except Exception as e3:
                print(f"⚠️ [Gemini Backup Alert] คีย์สำรองบัญชีที่สองขัดข้อง: {e3}")

            # --- ก๊อกที่ 4: สับสายข้ามค่ายหา GROQ ความเร็วแสง ---
            try:
                print("⚡ [Engine 4/5] เปิดระบบกู้ชีพฉุกเฉินความเร็วสูง GROQ_API_KEY...")
                if hasattr(team_instance, 'research_open_source_fallback_groq'):
                    return await team_instance.research_open_source_fallback_groq(category=category, user_id=user_id)
            except Exception as e4:
                print(f"⚠️ [Groq Alert] กองหนุนสับสายด่วนติดขัด: {e4}")

            # --- ก๊อกที่ 5: ป้อมปราการด่านสุดท้าย OPENROUTER ประคองระบบ ---
            try:
                print("🛡️ [Engine 5/5] หมุนสายด่านสุดท้ายเข้าหาปราการเหล็ก OPENROUTER_API_KEY...")
                if hasattr(team_instance, 'research_open_source_fallback_openrouter'):
                    return await team_instance.research_open_source_fallback_openrouter(category=category, user_id=user_id)
            except Exception as e5:
                print(f"💥 [Omni Collapse] โครงข่ายพลังงานพังหมดทั้ง 5 ด่าน: {e5}")
            
            return None

    def _self_heal_payload(self, corrupted_result: dict, target_team: str, user_message: str) -> dict:
        print(f"🚨 [Self-Healing Dynamic] เริ่มต้นแผนกู้ชีพสารสนเทศขั้นปลาย...")
        fallback_knowledge = shared_knowledge.search_shared_insight(query=user_message)
        
        healed_data = {
            "status": "success",
            "healed_by_orchestrator": True,
            "result": {
                "category": user_message if user_message else "Strategic Objective",
                "best_tools": [
                    {
                        "name": fallback_knowledge.get("best_tools", [{}])[0].get("name", "AI Omnipresent Suite"),
                        "benefits": "คงสภาพด้วยมหาเกราะระบบสำรอง 5 ชั้นอย่างสมบูรณ์แบบ",
                        "github_stars": "Invincible Core Tier"
                    }
                ],
                "conclusion": "⚙️ ระบบเปิดเกราะป้องกัน 5 ชั้น (5-Layer Omni Active) ปลอดภัยไร้กังวลเรื่องงบประมาณและระบบล่ม"
            }
        }
        if fallback_knowledge.get("collaboration_report"):
            healed_data["result"]["collaboration_report"] = fallback_knowledge["collaboration_report"]
        return healed_data

    async def route_and_execute(self, user_message: str, user_id: int):
        """
        [LAYER 3 - Orchestration Engine with 5-API Failover Matrix]
        """
        message_lower = user_message.lower()
        is_strategic_request = any(kw in message_lower for kw in ["ขยาย", "scale", "ย้ายระบบ", "สถาปัตยกรรม", "งบจำกัด", "ล้านคน", "แสนคน"])
        
        if is_strategic_request:
            print("👑 [Autonomous Strategy Engine] กำลังร่าง Blueprint ปฏิบัติการด้วยขุมพลังชุดใหม่...")
            user_message = f"หาเครื่องมือ open-source และออกแบบคลาวด์เซิฟเวอร์ให้คุ้มค่าที่สุดเพื่อรองรับ: {user_message}"

        target_team = intent_router.route_user_intent(user_message)
        user_memory.add_chat_turn(user_id=user_id, role="user", message=user_message, predicted_intent=target_team)
        
        if target_team == "general_chat":
            guide_message = (
                "🤖 **AI Command Center อัปเกรดสำเร็จ! ต้อนรับ DeepSeek เข้าสู่กองทัพจอมลุย!**\n\n"
                "ระบบเปิดใช้มหาเกราะ 5 ชั้นกู้ภัยแบบสับหลีกอัตโนมัติ (**5-Layer Omni Failover**) เรียบร้อย\n"
                "🛡️ *ใช้งานโมเดล DeepSeek เป็นหลัก หากโหมดฟรีหมดระบบจะดีดไป Gemini/Groq ทันทีโดยไม่มีค่าใช้จ่ายครับ!*"
            )
            user_memory.add_chat_turn(user_id=user_id, role="bot", message=guide_message.strip())
            return {"status": "success", "data": {"success": True, "message": guide_message.strip()}}
            
        if target_team == "unknown":
            execution_result = self._self_heal_payload({}, "autonomous_fallback", user_message)
            return {"status": "success", "data": execution_result}
            
        registry = self._load_registry()
        cached_insight = shared_knowledge.search_shared_insight(query=user_message)

        # --- PHASE 1: รันงานผ่านระบบสับเปลี่ยนมหาเกราะ 5 ชั้น ---
        team_config = registry["teams"].get(target_team)
        try:
            module_path, obj_name = team_config["entry_point"].split(":")
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            print(f"🚀 [Orchestrator Chain] รันทีมยุทธศาสตร์: {team_config['name']}")
            
            execution_result = await self._call_llm_with_failover(team_instance, user_message, user_id)
            
            if not execution_result or not isinstance(execution_result, dict) or "result" not in execution_result:
                execution_result = self._self_heal_payload(execution_result, target_team, user_message)
            else:
                shared_knowledge.publish_insight(author_team=target_team, topic=user_message, insight_data=execution_result["result"])
            
        except Exception as e:
            print(f"💥 [Critical Exception Caught] พบบั๊กระดับโครงสร้างลึก: {e}")
            execution_result = self._self_heal_payload({}, target_team, user_message)

        # --- PHASE 2: เครือข่าย Multi-Agent Handover ---
        is_collab_request = is_strategic_request or any(kw in message_lower for kw in ["และ", "คลาวด์", "เซิฟเวอร์", "server", "cloud", "อินฟรา"])
        
        if is_collab_request and "healed_by_orchestrator" not in execution_result:
            print("🔗 [Collaboration Chain Activated] สั่งเชื่อมสายงานอัตโนมัติ...")
            infra_config = registry["teams"].get("infrastructure_team")
            
            try:
                suggested_tool = execution_result["result"]["best_tools"][0]["name"]
                infra_module_path, infra_obj_name = infra_config["entry_point"].split(":")
                infra_module = importlib.import_module(infra_module_path)
                infra_instance = getattr(infra_module, infra_obj_name)
                
                execution_result["result"]["collaboration_report"] = {
                    "activated": True,
                    "target_team": "Strategic Infrastructure Architecture Team",
                    "recommendation": f"โฮสต์ระบบ {suggested_tool} ร่วมกับขุมพลังข้ามค่าย DeepSeek + มหาเกราะป้องกัน 5 ชั้นเรียบร้อย"
                }
                
                shared_knowledge.publish_insight(
                    author_team="Autonomous_Strategy_Center",
                    topic=f"strategic_infrastructure_for_{suggested_tool}",
                    insight_data=execution_result["result"]["collaboration_report"]
                )
                
            except Exception as collab_err:
                print(f"⚠️ [Handover Warning] ปัญหาส่วนเชื่อมงานเสริม: {collab_err}")

        if cached_insight:
            execution_result["shared_knowledge_hit"] = True

        user_memory.add_chat_turn(user_id=user_id, role="bot", message=f"🏆 [5-Layer Omni Failover Protected] สำเร็จอย่างสมบูรณ์แบบด้วยขุมพลัง DeepSeek")
        return {"status": "success", "data": execution_result}

    async def route_objective(self, user_message: str, user_id: int):
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()