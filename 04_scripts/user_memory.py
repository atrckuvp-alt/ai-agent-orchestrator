import json
from pathlib import Path
import datetime as dt

class UserMemory:
    def __init__(self):
        self.memory_dir = Path(__file__).resolve().parents[1] / "00_memory" / "user_memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def get_context(self, user_id: int) -> dict:
        file_path = self.memory_dir / f"user_{user_id}.json"
        if file_path.exists():
            try:
                return json.loads(file_path.read_text(encoding="utf-8"))
            except:
                pass
        return {"current_intent": "general", "summary_context": "", "extracted_entities": {}}

    def update_context(self, user_id: int, summary_context: str, current_intent: str, entities: dict = None):
        file_path = self.memory_dir / f"user_{user_id}.json"
        data = {
            "current_intent": current_intent,
            "summary_context": summary_context,
            "extracted_entities": entities or {},
            "last_updated": dt.datetime.now().isoformat()
        }
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

user_memory = UserMemory()