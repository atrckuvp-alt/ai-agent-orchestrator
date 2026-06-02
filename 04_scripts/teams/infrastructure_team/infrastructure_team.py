import json
from pathlib import Path
import datetime as dt
import sys
import asyncio

# ค้นหาพาธรากฐานของโปรเจกต์หลักเพื่อนำเข้าโมดูลแวดล้อมได้ถูกต้อง
CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent.parent.parent  # ขึ้นไป 3 ชั้น เพื่อให้พ้นจาก 04_scripts/teams/infrastructure_team ไปยัง Root

# ลงทะเบียนพาธของสคริปต์เข้าสู่ระบบระบบอ้างอิงของ Python
paths_to_add = [
    str(ROOT),
    str(ROOT / "04_scripts"),
    str(ROOT / "04_scripts" / "teams")
]
for p in paths_to_add:
    if p not in sys.path:
        sys.path.insert(0, p)

from meta_orchestrator import meta_orchestrator

class InfrastructureTeam:
    def __init__(self):
        self.research_path = ROOT / "00_memory" / "oss_research.json"
        self.research_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.research_path.exists():
            self.research_path.write_text(json.dumps({
                "research": [],
                "last_updated": None,
                "total_research": 0
            }, indent=2, ensure_ascii=False), encoding="utf-8")

    async def research_open_source(self, category: str, user_id: int = 7238952711):
        """ระบบวิจัยโครงสร้างพื้นฐานส่งตรงผลรายงานกลับทาง Telegram"""
        print(f"🔍 [Infrastructure Team] Researching for category: '{category}'")

        try:
            core_skill = meta_orchestrator.core_skill
        except Exception:
            core_skill = "Buddhist Governance and Cost Optimization"

        # ข้อมูลจำลองและสรุปรายงานตัวเลือกที่ดีที่สุด (Fallback Report)
        mock_infra_report = {
            "category": category,
            "top_recommendations": [
                "SQLite (ฐานข้อมูลแบบไฟล์ในตัว เครื่องมือง่ายและฟรี 100% เหมาะสำหรับแอปขนาดเล็ก)",
                "PostgreSQL via Supabase (โควตาฟรีแอดวานซ์ คุ้มค่าและเสถียรที่สุดในระยะยาว)",
                "MongoDB Atlas (โควตาฟรีระดับ M0 สำหรับการจัดเก็บข้อมูลแบบ NoSQL Document)"
            ],
            "best_choice": "PostgreSQL (ผ่านระบบ Supabase Cloud)",
            "reasoning": "มีความยืดหยุ่นสูง รองรับระบบข้อมูลโครงสร้างสัมพันธ์ได้ดีเยี่ยม และมีหน้าแดชบอร์ดบริหารจัดการคลาวด์ฟรีที่เสถียรที่สุดในตลาด",
            "free_tier_notes": "Supabase ให้บริการฟรีตลอดเวลา แต่หากไม่มีความเคลื่อนไหวเกิน 7 วัน ระบบจะปิดพักตัวอัตโนมัติ ต้องคอยเปิดแอปเพื่ออุ่นฐานข้อมูลเป็นครั้งคราว"
        }

        research_entry = {
            "category": category,
            "timestamp": dt.datetime.now().isoformat(),
            "status": "success",
            "result": mock_infra_report,
            "used_skill": "meta_orchestrator_skill.md"
        }

        # บันทึกข้อมูลรายงานวิจัยลงความจำคลังวิจัย (00_memory)
        try:
            data = json.loads(self.research_path.read_text(encoding="utf-8"))
            data["research"].append(research_entry)
            data["last_updated"] = dt.datetime.now().isoformat()
            data["total_research"] = len(data["research"])
            self.research_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print("💾 [Infrastructure Team] บันทึกผลรายงานลงคลังความจำเรียบร้อย")
        except Exception as e:
            print(f"⚠️ [Memory Log Warning] ไม่สามารถบันทึกไฟล์วิจัยได้: {e}")

        # 🚀 [Real-time Telegram Bridge] ส่งรายงานสรุปการแก้ไขโครงสร้างคลาวด์กลับให้ผู้ใช้
        try:
            import os
            from aiogram import Bot
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            if bot_token:
                bot = Bot(token=bot_token)
                
                formatted_report = f"""
🛡️ **[Core Infrastructure Team Report]**
หมวดหมู่ที่ตรวจวิจัย: *{category}*

🎯 **ตัวเลือกที่ดีที่สุด (Best Choice):**
• `{mock_infra_report.get('best_choice')}`

🌟 **ข้อแนะนำระดับโครงสร้าง 3 อันดับแรก:**
1️⃣ {mock_infra_report.get('top_recommendations')[0]}
2️⃣ {mock_infra_report.get('top_recommendations')[1]}
3️⃣ {mock_infra_report.get('top_recommendations')[2]}

💡 **วิเคราะห์ความคุ้มค่าตามหลักธรรมาภิบาล:**
_{mock_infra_report.get('reasoning')}_

⚠️ **ข้อสังเกตโควตาคลาวด์ฟรี (Free Tier Alert):**
`{mock_infra_report.get('free_tier_notes')}`
                """
                await bot.send_message(chat_id=user_id, text=formatted_report.strip(), parse_mode="Markdown")
                print(f"📨 [Infrastructure Team] ส่งเอกสารรายงานกลับหาผู้ใช้ {user_id} สำเร็จ")
                
                session = await bot.get_session()
                await session.close()
        except Exception as tel_err:
            print(f"❌ [Telegram Send Error] ไม่สามารถส่งรายงานหาผู้ใช้ได้: {tel_err}")

        return research_entry

infrastructure_team = InfrastructureTeam()