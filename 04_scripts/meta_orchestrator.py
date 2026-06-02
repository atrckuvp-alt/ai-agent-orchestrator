import json
from pathlib import Path
import datetime as dt

from provider_router import provider_router
from user_memory import user_memory

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"
SKILLS_DIR = MEMORY / "skills"

class MetaOrchestrator:
    def __init__(self):
        self.skill_path = SKILLS_DIR / "meta_orchestrator_skill.md"
        self.framework_path = SKILLS_DIR / "decision_framework.md"
        self.registry_path = MEMORY / "team_registry.json"
        
        SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        
        self._load_core_skill()
        self._load_decision_framework()
        self._init_registry()

    def _load_core_skill(self):
        try:
            self.core_skill = self.skill_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.core_skill = "Core Skill: Executive Orchestration and High-Level Coordination."

    def _load_decision_framework(self):
        try:
            if self.framework_path.exists():
                self.decision_framework = self.framework_path.read_text(encoding="utf-8")
                print("🎯 [Meta Orchestrator] Loaded Triple-Lens Decision Framework Successfully!")
            else:
                self.decision_framework = "Framework: Optimize for free tier, use systems thinking, and maintain legal safety."
                print("⚠️ [Warning] decision_framework.md not found in skills directory, using static framework.")
        except Exception as e:
            self.decision_framework = "Framework: Default parameters."
            print(f"⚠️ [Error] Cannot load framework: {e}")

    def _init_registry(self):
        """โหลดระบบจัดตั้งทีมแบบ Dynamic จากไฟล์ JSON Registry โดยตรง"""
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            default = {
                "meta_orchestrator": {
                    "status": "active",
                    "active_teams": ["infrastructure_team", "oss_research_team"]
                },
                "teams": {
                    "infrastructure_team": {
                        "name": "Infrastructure & Cloud DevOps Team",
                        "description": "รับผิดชอบการออกแบบ คํานวณต้นทุน และจัดการเซิร์ฟเวอร์ Cloud / Cost Optimization",
                        "capabilities": ["cloud_architecture_design", "cost_optimization"],
                        "entry_point": "teams.infrastructure_team.infrastructure_team:infrastructure_team"
                    }
                }
            }
            self.registry_path.write_text(json.dumps(default, indent=2, ensure_ascii=False), encoding="utf-8")

    def _get_registered_teams_description(self) -> str:
        """แปลงรายการทีมใน JSON ออกมาเป็น String เพื่อป้อนให้ LLM เลือกอย่างแม่นยำ"""
        try:
            registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
            teams_desc = []
            for t_id, t_info in registry.get("teams", {}).items():
                teams_desc.append(f"- '{t_id}': {t_info.get('description')} (Capabilities: {', '.join(t_info.get('capabilities', []))})")
            return "\n".join(teams_desc)
        except Exception:
            return "- 'infrastructure_team': Core Infrastructure AI Team"

    async def route_objective(self, objective: str, user_id: int = 7238952711) -> dict:
        print(f"🧠 [Meta Orchestrator] Executing Triple-Lens Decision Matrix via Team Registry...")
        
        mem_ctx = user_memory.get_context(user_id)
        past_summary = mem_ctx.get("summary_context", "ไม่มีประวัติคุยก่อนหน้า")
        past_entities = json.dumps(mem_ctx.get("extracted_entities", {}), ensure_ascii=False)
        
        # ดึงรายชื่อทีมปัจจุบันจากฐานระบบ JSON มามัดรวมใส่ Prompt
        available_teams_prompt = self._get_registered_teams_description()

        prompt = f"""
        คุณคือ Meta Orchestrator (COO + CTO) หน้าที่ของคุณคือวิเคราะห์ Objective ปัจจุบันของผู้ใช้
        โดยพิจารณาร่วมกับ "ประวัติการคุยย้อนหลัง" และต้องตัดสินใจภายใต้กรอบ "Decision Framework" อย่างเคร่งครัด

        ---
        [DECISION FRAMEWORK MATRIX]
        {self.decision_framework}
        ---
        [AVAILABLE TEAMS IN REGISTRY]
        {available_teams_prompt}
        ---
        [CONTEXT MEMORY]
        - ประวัติสาระสำคัญเดิม: {past_summary}
        - คีย์เวิร์ด/ตัวแปรในระบบ: {past_entities}
        ---
        คำสั่งปัจจุบันจากผู้ใช้: "{objective}"

        จงเลือกทีมงานปฏิบัติการที่เหมาะสมที่สุดจากรายการทีมที่มีอยู่จริงในระบบด้านบนเท่านั้น ห้ามคิดชื่อทีมขึ้นมาใหม่เองเด็ดขาด!
        เขียนอธิบายเหตุผล (Reason) สั้นๆ เชิงกลยุทธ์

        ให้ตอบกลับเฉพาะในรูปแบบ JSON โครงสร้างนี้เท่านั้น (ห้ามมี Markdown นอก JSON):
        {{
            "team": "ชื่อคีย์ของทีมที่เลือก (เช่น infrastructure_team หรือ oss_research_team)",
            "reason": "อธิบายเหตุผลเชิงกลยุทธ์ที่เชื่อมโยงกับ Decision Framework",
            "new_summary_context": "สรุปสาระสำคัญเพิ่มจากคำสั่งปัจจุบันสั้นๆ 1 ประโยคเพื่อจำต่อ",
            "extracted_entities": {{"key1": "value1"}}
        }}
        """
        
        try:
            ai_response = await provider_router.request_llm(prompt, tier="reasoning")
            cleaned_json = ai_response.replace("```json", "").replace("
```", "").strip()
            result_data = json.loads(cleaned_json)
            
            team = result_data.get("team", "infrastructure_team")
            reason = result_data.get("reason", "วิเคราะห์ผ่านระบบ Dynamic Team Registry")
            new_summary = result_data.get("new_summary_context", objective)
            
            raw_entities = result_data.get("extracted_entities", {})
            formatted_entities = {
                "teams": [team] if team else [],
                "workflows": [raw_entities.get("workflow")] if isinstance(raw_entities.get("workflow"), str) else raw_entities.get("workflows", []),
                "open_source": raw_entities.get("tools", []) or raw_entities.get("open_source", []),
                "keywords": raw_entities.get("keywords", [])
            }

            user_memory.update_context(
                user_id=user_id, 
                summary_context=new_summary, 
                current_intent=team, 
                entities=formatted_entities
            )
            
        except Exception as e:
            print(f"⚠️ [Fallback] Switch to Registry Default due to error: {e}")
            team = "infrastructure_team"
            reason = f"Registry Fallback: ระบบเลือกทีมพื้นฐานความปลอดภัยสูง ({str(e)})"
            
            user_memory.update_context(
                user_id=user_id, 
                summary_context=objective, 
                current_intent=team, 
                entities={"teams": [team], "workflows": [], "open_source": [], "keywords": []}
            )

        print(f"→ Routed to Dynamic Team: {team} | Reason: {reason}")
        return {
            "team": team,
            "reason": reason,
            "objective": objective
        }

meta_orchestrator = MetaOrchestrator()