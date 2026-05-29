import json
from pathlib import Path
import datetime as dt
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "04_scripts"))

from meta_orchestrator import meta_orchestrator

class InfrastructureTeam:
    def __init__(self):
        self.research_path = Path(__file__).resolve().parents[2] / "00_memory" / "oss_research.json"
        self.research_path.parent.mkdir(exist_ok=True)
        
        if not self.research_path.exists():
            self.research_path.write_text(json.dumps({
                "research": [],
                "last_updated": None,
                "total_research": 0
            }, indent=2, ensure_ascii=False), encoding="utf-8")

    async def research_open_source(self, category: str):
        """Core Infrastructure Team - วิจัย OSS Tools จริง"""
        print(f"🔍 Infrastructure Team researching: {category}")

        core_skill = meta_orchestrator.get_core_skill()

        prompt = f"""
You are an expert OSS Researcher with Buddhist governance mindset.

Core Principles:
{core_skill[:700]}

Category: {category}

Find the best open-source and free-tier tools.
Focus on quality, stability, community, and ease of use.

Return JSON only:
{{
  "category": "{category}",
  "top_recommendations": ["tool1", "tool2", "tool3"],
  "best_choice": "recommended_tool",
  "reasoning": "เหตุผลตามหลักวิมังสาและความยั่งยืน",
  "free_tier_notes": "ข้อควรระวัง free tier"
}}
"""

        from run_orchestrator import call_openrouter_model
        result = call_openrouter_model("openrouter/free", prompt)

        research_entry = {
            "category": category,
            "timestamp": dt.datetime.now().isoformat(),
            "status": "success",
            "raw_result": result.get("content", str(result)),
            "used_skill": "meta_orchestrator_skill.md"
        }

        # บันทึก
        data = json.loads(self.research_path.read_text(encoding="utf-8"))
        data["research"].append(research_entry)
        data["last_updated"] = dt.datetime.now().isoformat()
        data["total_research"] = len(data["research"])
        self.research_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        print(f"✅ Infrastructure Team completed research on '{category}'")
        return research_entry

infrastructure_team = InfrastructureTeam()