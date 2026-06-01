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
        # เพิ่มพาร์ทสำหรับอ่านไฟล์ Decision Framework ใหม่
        self.framework_path = SKILLS_DIR / "decision_framework.md"
        self.registry_path = MEMORY / "team_registry.json"
        
        # สร้างโฟลเดอร์เผื่อไว้กรณีระบบติดตั้งใหม่
        SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        
        self._load_core_skill()
        self._load_decision_framework()
        self._init_registry()
        
        # ลงทะเบียนทีมหลัก
        self.register_team("infrastructure_team", "Core AI Infrastructure - OSS Research & Benchmark", ["research_agent", "benchmark_agent"])
        self.register_team("research_team", "Deep Research & Analysis Team", ["research_agent"])
        self.register_team("coding_team", "Coding & Development Team", ["coding_agent"])
        self.register_team("full_stack_team", "Full Stack AI Solution Team", ["research_agent", "coding_agent", "orchestrator"])

    def _load_core_skill(self):
        try:
            self.core_skill = self.skill_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.core_skill = "Core Skill: Executive Orchestration and High-Level Coordination."

    def _load_decision_framework(self):
        """โหลดพิมพ์เขียวกรอบแนวคิดการตัดสินใจเข้าสู่หน่วยความจำหลัก"""
        try:
            if self.framework_path.exists():
                self.decision_framework = self.framework_path.read_text(encoding="utf-8")
                print("🎯 [Meta Orchestrator] Loaded Triple-Lens Decision Framework Successfully!")
            else:
                # Fallback หากไฟล์ยังไม่ถูกเขียนย้ายไปโฟลเดอร์เป้าหมาย
                self.decision_framework = "Framework: Optimize for free tier, use systems thinking, and maintain legal safety."
                print("⚠️ [Warning] decision_framework.md not found in skills directory, using static framework.")
        except Exception as e:
            self.decision_framework = "Framework: Default parameters."
            print(f"⚠️ [Error] Cannot load framework: {e}")

    def _init_registry(self):
        if not self.registry_path.exists():
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            default = {
                "meta_orchestrator": {
                    "status": "active",
                    "active_teams": []
                },
                "teams": {}
            }
            self.registry_path.write_text(json.dumps(default, indent=2, ensure_ascii=False), encoding="utf-8")

    async def route_objective(self, objective: str, user_id: int = 7238952711) -> dict:
        print(f"🧠 [Meta Orchestrator] Executing Triple-Lens Decision Matrix...")
        
        mem_ctx = user_memory.get_context(user_id)
        past_summary = mem_ctx.get("summary_context", "ไม่มีประวัติคุยก่อนหน้า")
        past_entities = json.dumps(mem_ctx.get("extracted_entities", {}), ensure_ascii=False)

        # ผสานเอา Decision Framework เข้าไปขนาบข้างระบบความคิดของ Prompt
        prompt = f"""
        คุณคือ Meta Orchestrator (COO + CTO) หน้าที่ของคุณคือวิเคราะห์ Objective ปัจจุบันของผู้ใช้
        โดยพิจารณาร่วมกับ "ประวัติการคุยย้อนหลัง" และต้องตัดสินใจภายใต้กรอบ "Decision Framework" อย่างเคร่งครัด

        ---
        [DECISION FRAMEWORK MATRIX]
        {self.decision_framework}
        ---
        [CORE SKILL]
        {self.core_skill}
        ---
        [CONTEXT MEMORY]
        - ประวัติสาระสำคัญเดิม: {past_summary}
        - คีย์เวิร์ด/ตัวแปรในระบบ: {past_entities}
        ---
        คำสั่งปัจจุบันจากผู้ใช้: "{objective}"

        จงเลือกทีมที่เหมาะสมที่สุดตามหลักการ และเขียนอธิบายเหตุผล (Reason) 
        โดยให้ระบุชัดเจนว่าสอดคล้องกับกรอบแนวคิดใน Decision Framework อย่างไร (เช่น สอดคล้องกับเลนบริหาร/หลักวิมังสา/ความคุ้มค่า Free-tier)

        ให้ตอบกลับเฉพาะในรูปแบบ JSON โครงสร้างนี้เท่านั้น (ห้ามมี Markdown นอก JSON):
        {{
            "team": "ชื่อทีมที่เลือก (infrastructure_team, research_team, coding_team, full_stack_team)",
            "reason": "อธิบายเหตุผลเชิงกลยุทธ์ที่เชื่อมโยงกับ Decision Framework สั้นๆ",
            "new_summary_context": "สรุปสาระสำคัญเพิ่มจากคำสั่งปัจจุบันสั้นๆ 1 ประโยคเพื่อจำต่อ",
            "extracted_entities": {{"key1": "value1"}}
        }}
        """
        
        try:
            ai_response = await provider_router.request_llm(prompt, tier="reasoning")
            
            # แก้ไขส่วน cleaned_json ให้ถูกต้อง (สำคัญ!)
            cleaned_json = ai_response.replace("```json", "").replace("```", "").strip()
            result_data = json.loads(cleaned_json)
            
            team = result_data.get("team", "full_stack_team")
            reason = result_data.get("reason", "วิเคราะห์ผ่านระบบ Triple-Lens Framework")
            new_summary = result_data.get("new_summary_context", objective)
# =====================================================================
# ✅ วางโค้ดชุดนี้แทนที่บล็อกจัดการ Entities และ Exception ด้านล่างของฟังก์ชัน route_to_team
# =====================================================================
            # 🔗 [เริ่มจุดแทรกแทนที่] สกัดและปรับรูปแบบ Entities ให้เข้ากับโครงสร้าง Long-Term Memory
            raw_entities = result_data.get("extracted_entities", {})
            
            # ทำการ Flat แขนงข้อมูลเพื่อให้จัดเก็บลง Keyword Index ของ AI-BOS ได้ง่ายและไม่ซ้ำซ้อน
            formatted_entities = {
                "teams": [team] if team else [],
                "workflows": [raw_entities.get("workflow")] if isinstance(raw_entities.get("workflow"), str) else raw_entities.get("workflows", []),
                "open_source": raw_entities.get("tools", []) or raw_entities.get("open_source", []),
                "keywords": raw_entities.get("keywords", [])
            }

            # บันทึกข้อมูลเข้าสู่ Unified Core Memory (เชื่อมเข้ากับ memory_manager อัตโนมัติ)
            user_memory.update_context(
                user_id=user_id, 
                summary_context=new_summary, 
                current_intent=team, 
                entities=formatted_entities
            )
            
        except Exception as e:
            print(f"⚠️ [Fallback] Switch to Static Rules due to error: {e}")
            team = "full_stack_team"
            reason = f"Static Fallback: ระบบเลือกทีมกลางเพื่อความปลอดภัยสูงสุด ({str(e)})"
            
            # กรณีเอิร์รอร์จากตัวโมเดล ให้ทำ Fallback บันทึกค่าเซฟตี้พื้นฐานเพื่อไม่ให้ Process หลักหยุดทำงาน
            user_memory.update_context(
                user_id=user_id, 
                summary_context=objective, 
                current_intent=team, 
                entities={"teams": [team], "workflows": [], "open_source": [], "keywords": []}
            )

        print(f"→ Routed to: {team} | Reason: {reason}")
        return {
            "team": team,
            "reason": reason,
            "objective": objective
        }

    def register_team(self, team_name: str, description: str, agents: list):
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        registry["teams"][team_name] = {
            "name": team_name,
            "description": description,
            "agents": agents,
            "created_at": dt.datetime.now().isoformat(),
            "status": "active"
        }
        if team_name not in registry["meta_orchestrator"]["active_teams"]:
            registry["meta_orchestrator"]["active_teams"].append(team_name)
        self.registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
        return registry["teams"][team_name]

meta_orchestrator = MetaOrchestrator()