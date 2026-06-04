# Complete file: 04_scripts/shared_knowledge.py (With Plan C Auto-Cleaning Engine)
import json
from pathlib import Path
import datetime

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
KNOWLEDGE_PATH = ROOT / "00_memory" / "shared_knowledge.json"

class SharedKnowledgeBase:
    def __init__(self):
        self._ensure_knowledge_base_exists()
        # จำกัดขนาดความรู้ในฐานข้อมูลฟรีสูงสุด 50 หัวข้อหลัก เพื่อความเบาและเร็ว
        self.MAX_KNOWLEDGE_ENTRIES = 50 

    def _ensure_knowledge_base_exists(self):
        KNOWLEDGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not KNOWLEDGE_PATH.exists():
            default_base = {
                "insights": [
                    {
                        "topic": "baseline_infrastructure",
                        "author_team": "Infrastructure_Core",
                        "best_tools": [{"name": "SQLite + Supabase", "benefits": "ประหยัดงบ 0 บาท รองรับเสถียรภาพระดับสูง"}],
                        "conclusion": "โครงสร้างพื้นฐานเริ่มต้นสแตนด์บายเรียบร้อย",
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                ]
            }
            KNOWLEDGE_PATH.write_text(json.dumps(default_base, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_knowledge(self) -> dict:
        try:
            return json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"insights": []}

    def _save_knowledge(self, data: dict):
        KNOWLEDGE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def search_shared_insight(self, query: str) -> dict:
        """📦 ค้นหาคลังความรู้ส่วนกลางเพื่อนำไปใช้เสริมความฉลาดให้ตัวหลัก"""
        kb = self._load_knowledge()
        query_lower = query.lower()
        
        for entry in kb.get("insights", []):
            if entry.get("topic", "").lower() in query_lower or query_lower in entry.get("topic", "").lower():
                print(f"🎯 [Knowledge Hit] พบข้อมูลเก่าที่สามารถนำมา Reuse ได้ทันทีในหัวข้อ: {entry['topic']}")
                return entry
        return {}

    def publish_insight(self, author_team: str, topic: str, insight_data: dict):
        """🚀 บันทึกองค์ความรู้ใหม่ พร้อมเปิดระบบสแกนล้างข้อมูลล้าสมัยอัตโนมัติ (Plan C)"""
        kb = self._load_knowledge()
        
        # ปรับรูปแบบข้อมูลใหม่เตรียมยัดลงคลัง
        new_entry = {
            "topic": topic,
            "author_team": author_team,
            "best_tools": insight_data.get("best_tools", []),
            "conclusion": insight_data.get("conclusion", "ประมวลผลสำเร็จ"),
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 🧼 [PLAN C - DUPLICATE EXTRACTION] ลบข้อมูลหัวข้อเดียวกันของเก่าออกก่อน (ป้องกันข้อมูลขยะซ้ำซ้อน)
        filtered_insights = [e for e in kb.get("insights", []) if e.get("topic", "").lower() != topic.lower()]
        filtered_insights.append(new_entry)
        
        kb["insights"] = filtered_insights
        
        # 🧼 [PLAN C - AUTO-CLEANING MATRIX] 
        # ถ้าความรู้บวมเกินลิมิตที่ตั้งไว้ ระบบจะทำการตัดลบข้อมูลที่ "เก่าที่สุด" (FIFO) ทิ้งทันทีเพื่อเซฟพื้นที่
        if len(kb["insights"]) > self.MAX_KNOWLEDGE_ENTRIES:
            print(f"🧹 [Plan C Auto-Cleaning] คลังปัญญาเริ่มมีความหนาแน่นเกิน {self.MAX_KNOWLEDGE_ENTRIES} รายการ! ทำการจัดระเบียบโครงสร้างใหม่...")
            # เรียงลำดับตามเวลา ใครเก่าสุดโดนดีดออก
            kb["insights"].sort(key=lambda x: x.get("timestamp", ""))
            while len(kb["insights"]) > self.MAX_KNOWLEDGE_ENTRIES:
                removed = kb["insights"].pop(0)
                print(f"🗑️ [Self-Healed Storage] ลบสารสนเทศเก่าเก็บ: '{removed.get('topic')}' เพื่อคงความเบาให้ระบบ")
                
        self._save_knowledge(kb)
        print(f"📝 [Knowledge Published] บันทึกและจัดระเบียบปัญญาในหัวข้อ '{topic}' เรียบร้อย")

shared_knowledge = SharedKnowledgeBase()