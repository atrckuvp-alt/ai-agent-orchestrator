import json
from pathlib import Path
import datetime as dt

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
            registry = {
                "meta_orchestrator": {
                    "version": "1.0",
                    "created_at": dt.datetime.now().isoformat(),
                    "active_teams": [],
                    "governance": {
                        "use_traidharma": True,
                        "use_iddhipada": True,
                        "pdpa_compliant": True,
                        "prefer_open_source": True,
                        "approval_required": True
                    }
                },
                "teams": {}
            }
            self.registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    def route_objective(self, objective: str):
        """Meta Orchestrator วิเคราะห์และกำหนดทีมด้วย Core Skill"""
        print(f"🧠 Meta Orchestrator analyzing: {objective[:80]}...")

        lower_obj = objective.lower()

        # ใช้ Core Skill ในการคิด (Systems Thinking + วิมังสา)
        if any(word in lower_obj for word in ["วิจัย", "หา", "analyze", "research", "ศึกษ"]):
            team = "research_team"
            reason = "เป็นงานวิจัยและหาข้อมูล"
        elif any(word in lower_obj for word in ["พัฒนา", "coding", "build", "สร้างโค้ด", "โปรแกรม"]):
            team = "coding_team"
            reason = "เป็นงานพัฒนาและเขียนโค้ด"
        elif any(word in lower_obj for word in ["ธุรกิจ", "branding", "ตลาด", "ขาย", "การตลาด"]):
            team = "branding_team"
            reason = "เป็นงานธุรกิจและแบรนด์ดิ้ง"
        else:
            team = "full_stack_team"
            reason = "เป็นงานทั่วไป ใช้ทีมครบวงจร"

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

    def get_team(self, team_name: str):
        registry = json.loads(self.registry_path.read_text(encoding="utf-8"))
        return registry["teams"].get(team_name)

meta_orchestrator = MetaOrchestrator()  # ทำมาค