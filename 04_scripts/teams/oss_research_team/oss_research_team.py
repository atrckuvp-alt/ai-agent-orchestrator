import json
from pathlib import Path
import datetime as dt
import sys

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent.parent.parent

paths_to_add = [str(ROOT), str(ROOT / "04_scripts")]
for p in paths_to_add:
    if p not in sys.path:
        sys.path.insert(0, p)

class OSSResearchTeam:
    def __init__(self):
        self.research_path = ROOT / "00_memory" / "oss_research.json"
        self.research_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.research_path.exists():
            self.research_path.write_text(json.dumps({
                "research": [],
                "last_updated": None,
                "total_research": 0
            }, indent=2, ensure_ascii=False), encoding="utf-8")

    async def research_open_source(self, category: str, user_id: int):
        """[OSS Research Team] จัดทำรายงานสรุปซอฟต์แวร์โอเพนซอร์สยอดนิยม"""
        print(f"🛰️ [OSS Research Team] เริ่มทำการค้นคว้าหมวดหมู่เครื่องมือ: '{category}'")

        mock_oss_report = {
            "category": category,
            "best_tools": [
                {
                    "name": "n8n (Workflow Automation)",
                    "benefits": "ตัวเชื่อมต่อ API ยืดหยุ่นสูงสุด รันบน Docker ส่วนตัวฟรี ทดแทน Zapier/Make ช่วยเซฟงบหลักแสน",
                    "github_stars": "42k Stars"
                },
                {
                    "name": "Mautic (Marketing Automation)",
                    "benefits": "ระบบบริหารจัดการแคมเปญการตลาด ส่งอีเมล ทำ Segment ลูกค้าฟรี ไม่มีค่าลิขสิทธิ์รายเดือน",
                    "github_stars": "6.5k Stars"
                }
            ],
            "conclusion": "หากต้องการต่อท่อระบบ Automation แนะนำ n8n คุ้มค่าที่สุด ส่วน Mautic เหมาะสำหรับงาน CRM และ Email Marketing ครับ"
        }

        research_entry = {
            "category": category,
            "timestamp": dt.datetime.now().isoformat(),
            "status": "success",
            "result": mock_oss_report
        }

        # บันทึกลงคลังข้อมูลประวัติศาสตร์ฝั่งหลังบ้าน
        try:
            data = json.loads(self.research_path.read_text(encoding="utf-8"))
            data["research"].append(research_entry)
            data["last_updated"] = dt.datetime.now().isoformat()
            data["total_research"] = len(data["research"])
            self.research_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"⚠️ [OSS Storage Error] {e}")

        # 🚀 ยิงข้อความรายงานเข้า Telegram สดๆ เรียลไทม์
        try:
            import os
            from aiogram import Bot
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            if bot_token:
                bot = Bot(token=bot_token)
                formatted_report = f"""
🛰️ **[Open-Source Scouting Team Report]**
หมวดหมู่ซอฟต์แวร์ที่ตรวจค้น: *{category}*

🌟 **สุดยอดเครื่องมือ Open-Source ที่แนะนำ:**
1️⃣ **{mock_oss_report['best_tools'][0]['name']}**
• จุดเด่น: _{mock_oss_report['best_tools'][0]['benefits']}_
• GitHub Stars: `{mock_oss_report['best_tools'][0]['github_stars']}`

2️⃣ **{mock_oss_report['best_tools'][1]['name']}**
• จุดเด่น: _{mock_oss_report['best_tools'][1]['benefits']}_
• GitHub Stars: `{mock_oss_report['best_tools'][1]['github_stars']}`

💡 **บทสรุปจากทีมวิจัย:**
`{mock_oss_report['conclusion']}`
                """
                await bot.send_message(chat_id=user_id, text=formatted_report.strip(), parse_mode="Markdown")
                print(f"📨 [OSS Research Team] ส่งรายงานให้ผู้ใช้ {user_id} สำเร็จ")
                await bot.session.close()
        except Exception as tel_err:
            print(f"❌ [Telegram Send Error] {tel_err}")

        return research_entry

oss_research_team = OSSResearchTeam()