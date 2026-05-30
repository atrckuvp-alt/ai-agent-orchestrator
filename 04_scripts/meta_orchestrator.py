import json
from pathlib import Path
import datetime as dt

# 1. แทรกการอิมพอร์ต ProviderRouter ที่สร้างไว้
from provider_router import provider_router

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"

class MetaOrchestrator:
    def __init__(self):
        self.skill_path = MEMORY / "skills" / "meta_orchestrator_skill.md"
        self.registry_path = MEMORY / "team_registry.json"
        self._load_core_skill()
        self._init_registry()
        # ลงทะเบียนทีมหลัก
        self.register_team("infrastructure_team", "Core AI Infrastructure - OSS Research & Benchmark", ["research_agent", "benchmark_agent"])
        self.register_team("research_team", "Deep Research & Analysis Team", ["research_agent"])
        self.register_team("coding_team", "Coding & Development Team", ["coding_agent"])
        self.register_team("full_stack_team", "Full Stack AI Solution Team", ["research_agent", "coding_agent", "orchestrator"])

    def _load_core_skill(self):
        """โหลด Core Skill ตลอดเวลา"""
        try:
            self.core_skill = self.skill_path.read_text(encoding="utf-8")
            print("✅ Meta Orchestrator loaded Core Skills (ศุภจี + พุทธ + กฎหมายไทย)")
        except FileNotFoundError:
            self.core_skill = "Core Skill not found"
            print("⚠️ Warning: meta_orchestrator_skill.md not found")

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

    # 2. ปรับปรุงฟังก์ชันนี้ให้เรียกใช้คุณสมบัติสลับค่ายอัตโนมัติ (Async AI Reasoning)
    async def route_objective(self, objective: str) -> dict:
        """
        อัปเกรดใช้ระบบวิเคราะห์เป้าหมายผ่าน LLM พร้อมโครงสร้างรองรับ Failover Tier
        """
        print(f"🧠 [Meta Orchestrator] Analyzing Objective using Smart LLM Router...")
        
        # วาง System Prompt ครอบลอจิกอิทธิบาท 4 + วิมังสา ควบคุมการทำงาน
        prompt = f"""
        คุณคือ Meta Orchestrator (COO + CTO) หน้าที่ของคุณคือวิเคราะห์ Objective ของผู้ใช้ 
        แล้วเลือกทีมที่เหมาะสมที่สุดจากรายการทีมที่ลงทะเบียนไว้ด้านล่างนี้ 
        และให้เหตุผลในการเลือกโดยยึดหลัก Systems Thinking และ ความเหมาะสมตามความจริง

        Core Skill Context ของคุณ:
        {self.core_skill}

        รายการทีมที่มีในระบบ:
        1. infrastructure_team: งานวิจัย Open Source Tools, ตรวจสอบ Benchmark โครงสร้างพื้นฐาน
        2. research_team: งานวิเคราะห์ข้อมูลเชิงลึก ค้นคว้าข้อมูลทั่วไป
        3. coding_team: งานเขียนโค้ด พัฒนาซอฟต์แวร์ ตรวจสอบ Bug
        4. full_stack_team: งานระบบใหญ่ ครบวงจรที่ต้องใช้ทั้งวิจัยและเขียนโค้ดร่วมกัน

        คำสั่งจากผู้ใช้: "{objective}"

        ให้ตอบกลับเฉพาะในรูปแบบ JSON รูปแบบนี้เท่านั้น (ห้ามมีคำอธิบายอื่นนอก JSON):
        {{
            "team": "ชื่อทีมที่เลือก (ต้องเลือกจาก 4 ทีมด้านบนเท่านั้น)",
            "reason": "เหตุผลสั้นๆ ในการเลือกทีมนี้"
        }}
        """
        
        try:
            # ยิงผ่านประตูเซ็ตความสามารถสูง (Reasoning Tier) ถ้าค่ายไหนล่มจะสลับหลังบ้านทันที
            ai_response = await provider_router.request_llm(prompt, tier="reasoning")
            
            # คลีนผลลัพธ์เผื่อ AI แอบใส่เครื่องหมาย markdown block มา
            cleaned_json = ai_response.replace("```json", "").replace("```", "").strip()
            result_data = json.loads(cleaned_json)
            
            team = result_data.get("team", "full_stack_team")
            reason = result_data.get("reason", "เลือกใช้ทีมครอบวงจรเนื่องจากคำสั่งมีความซับซ้อน")
            
        except Exception as e:
            # Fallback Plan: หากระบบ LLM เกิดปัญหาพร้อมกันทั้งหมด ให้ใช้กฎแบบเดิมทำงานแทนเพื่อป้องกันระบบหยุดชงัก
            print(f"⚠️ [Fallback Triggered] LLM Failover Layer Maxed Out, switching to Static Rules: {e}")
            lower = objective.lower()
            if any(k in lower for k in ["วิจัย", "research", "oss"]):
                team = "infrastructure_team"
                reason = "Static Fallback: ตรวจพบคำสำคัญด้านการวิจัยระบบ"
            elif any(k in lower for k in ["โค้ด", "code", "เขียนโปรแกรม", "develop"]):
                team = "coding_team"
                reason = "Static Fallback: ตรวจพบคำสำคัญด้านการเขียนโปรแกรม"
            else:
                team = "full_stack_team"
                reason = "Static Fallback: งานทั่วไป"

        print(f"→ Routed to: {team} | Reason: {reason}")
        return {
            "team": team,
            "reason": reason,
            "objective": objective
        }

    def get_core_skill(self):
        """ส่ง Core Skill ให้ Agent อื่นใช้"""
        return self.core_skill

    def register_team(self, team_name: str, description: str, agents: list):
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        
        registry["teams"][team_name] = {
            "name": team_name,
            "description": description,
            "agents": agents,
            "created_at": dt.datetime.now().isoformat(),
            "status": "active",
            "core_skill_reference": "meta_orchestrator_skill.md"
        }
        
        if team_name not in registry["meta_orchestrator"]["active_teams"]:
            registry["meta_orchestrator"]["active_teams"].append(team_name)
        
        self.registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ Registered team: {team_name} | Description: {description[:60]}...")
        return registry["teams"][team_name]