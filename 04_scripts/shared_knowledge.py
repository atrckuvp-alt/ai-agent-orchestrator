# Complete file: 04_scripts/shared_knowledge.py (Bulletproof & Safe JSON Database)
import json
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
KNOWLEDGE_BASE_PATH = ROOT / "00_memory" / "shared_knowledge_base.json"

class SharedKnowledge:
    def __init__(self):
        self._ensure_knowledge_base_exists()

    def _ensure_knowledge_base_exists(self):
        KNOWLEDGE_BASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not KNOWLEDGE_BASE_PATH.exists():
            initial_data = {"insights": []}
            KNOWLEDGE_BASE_PATH.write_text(json.dumps(initial_data, indent=2, ensure_ascii=False), encoding="utf-8")

    def publish_insight(self, author_team: str, topic: str, insight_data: dict):
        try:
            try:
                data = json.loads(KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8"))
            except Exception:
                data = {"insights": []}

            if "insights" not in data:
                data["insights"] = []

            new_insight = {
                "author_team": str(author_team),
                "topic": str(topic),
                "tools": insight_data.get("best_tools", []),
                "conclusion": insight_data.get("conclusion", "ไม่มีข้อมูลบทสรุป")
            }
            data["insights"].append(new_insight)
            KNOWLEDGE_BASE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"✅ [Shared Knowledge] บันทึกแผนงานหัวข้อ '{topic}' สำเร็จ")
            return True
        except Exception as e:
            print(f"❌ [Shared Knowledge Error] บันทึกพลาด: {e}")
            return False

shared_knowledge = SharedKnowledge()