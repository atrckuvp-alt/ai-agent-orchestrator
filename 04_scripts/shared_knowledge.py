# Create a new file: 04_scripts/shared_knowledge.py
import json
from pathlib import Path
from datetime import datetime

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
KNOWLEDGE_PATH = ROOT / "00_memory" / "shared_knowledge.json"

class SharedKnowledgeEngine:
    def __init__(self):
        KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not KNOWLEDGE_PATH.exists():
            self._save_knowledge({"articles": []})

    def _load_knowledge(self) -> dict:
        try:
            return json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"articles": []}

    def _save_knowledge(self, data: dict):
        KNOWLEDGE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def publish_insight(self, author_team: str, topic: str, insight_data: dict):
        """
        [LAYER 4 - Knowledge Publishing API]
        ให้เอเจนต์คลังย่อยส่งข้อมูลเชิงลึกมาเก็บไว้ในสมองส่วนกลาง
        """
        knowledge = self._load_knowledge()
        
        new_entry = {
            "id": f"kn_{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "author": author_team,
            "topic": topic.lower().strip(),
            "insight": insight_data
        }
        
        # ตรวจสอบเพื่อไม่ให้บันทึกหัวข้อซ้ำซ้อนเกินไป
        knowledge["articles"] = [a for a in knowledge["articles"] if a["topic"] != new_entry["topic"]]
        knowledge["articles"].append(new_entry)
        self._save_knowledge(knowledge)
        print(f"🧠 [Shared Knowledge] Team '{author_team}' successfully published new insight on topic: '{topic}'")

    def search_shared_insight(self, query: str) -> dict:
        """
        [LAYER 4 - Knowledge Query Retrieval]
        ค้นหาข้อมูลเชิงลึกที่เอเจนต์ตัวอื่นเคยวิจัยไว้เพื่อนำมาใช้เป็น Context เสริม
        """
        knowledge = self._load_knowledge()
        query_lower = query.lower()
        
        # ค้นหาแบบ Simple Keyword Match สำหรับความรู้ส่วนกลาง
        for article in knowledge["articles"]:
            if article["topic"] in query_lower or query_lower in article["topic"]:
                print(f"📖 [Shared Knowledge Hit!] Found relevant insight from '{article['author']}' about '{article['topic']}'")
                return article["insight"]
                
        return {}

shared_knowledge = SharedKnowledgeEngine()