import json
from pathlib import Path
import datetime as dt

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"

class TeamManager:
    def __init__(self):
        self.teams_dir = MEMORY / "active_teams"
        self.teams_dir.mkdir(exist_ok=True)

    def save_team(self, team_id: str, data: dict):
        """บันทึกข้อมูลทีม"""
        path = self.teams_dir / f"{team_id}.json"
        data["updated_at"] = dt.datetime.now().isoformat()
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def get_team(self, team_id: str):
        """ดึงข้อมูลทีม"""
        path = self.teams_dir / f"{team_id}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def list_teams(self):
        """แสดงทีมทั้งหมด"""
        teams = []
        for file in self.teams_dir.glob("*.json"):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                teams.append(data)
            except:
                continue
        return teams

team_manager = TeamManager()