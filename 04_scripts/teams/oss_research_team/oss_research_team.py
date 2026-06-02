import json
from pathlib import Path
import datetime as dt
import sys

# ดึงคลาสพิมพ์ใหญ่เข้ามาเพื่อใช้อ้างอิง Core Skill
from meta_orchestrator import MetaOrchestrator

meta_orchestrator = MetaOrchestrator()

class OSSResearchTeam:
    def __init__(self):
        # จุดเก็บไฟล์ผลลัพธ์การวิจัยของทีม OSS
        self.research_path = Path(__file__).resolve().parents[2] / "00_memory" / "oss_research_reports.json"
        self.research_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.research_path.exists():
            self.research_path.write_text(json.dumps({
                "reports": [],
                "last_updated": None,
                "total_reports": 0
            }, indent=2, ensure_ascii=False), encoding="utf-8")

    async def research_open_source(self, category: str):
        """ทีมวิจัยซอฟต์แวร์โอเพ่นซอร์ส - ทำการวิจัยและประเมินผลเครื่องมือจริงผ่าน LLM"""
        print(f"🔬 [OSS Research Team] Starting deep research on category: '{category}'")

        # ดึงพิมพ์เขียวกระบวนการคิดและข้อจำกัดเรื่อง Free-tier จากสมองส่วนกลาง
        core_skill = meta_orchestrator.core_skill
        decision_framework = meta_orchestrator.decision_framework

        prompt = f"""
        คุณคือหัวหน้าทีม OSS Research Specialist ผู้เชี่ยวชาญด้านการคัดสรรเทคโนโลยี Open Source ระดับโลก
        หน้าที่ของคุณคือวิเคราะห์และแนะนำเครื่องมือในหมวดหมู่ที่ผู้ใช้ร้องขอ โดยต้องคิดภายใต้กรอบแนวคิดนี้อย่างเคร่งครัด:

        [CORE PRINCIPLES & FRAMEWORK]
        {core_skill}
        {decision_framework}

        [หมวดหมู่ที่ต้องวิจัย]
        {category}

        จงค้นหาเครื่องมือ Open Source ที่ดีที่สุด 3 อันดับแรก (เน้นที่มี Free-tier หรือใช้งานได้ฟรีอย่างยั่งยืน ไม่มีค่าใช้จ่ายแอบแฝง มีชุมชนรองรับแข็งแกร่ง)
        พร้อมทำการวิเคราะห์ข้อดี ข้อเสีย และสรุปตัวเลือกที่ดีที่สุด (Best Choice) ตามหลักการบริหารความคุ้มค่า

        ให้ตอบกลับเฉพาะในรูปแบบ JSON โครงสร้างนี้เท่านั้น (ห้ามมี Markdown นอก JSON):
        {{
          "category": "{category}",
          "top_recommendations": ["ชื่อเครื่องมือ 1", "ชื่อเครื่องมือ 2", "ชื่อเครื่องมือ 3"],
          "best_choice": "ชื่อเครื่องมือที่แนะนำที่สุด",
          "reasoning": "เหตุผลเชิงกลยุทธ์และความคุ้มค่า",
          "free_tier_notes": "ข้อควรระวังหรือข้อจำกัดของเวอร์ชันฟรี"
        }}
        """

        try:
            # เรียกใช้งานโมดูล Router ของระบบหลักเพื่อยิงหา LLM
            from provider_router import provider_router
            ai_response = await provider_router.request_llm(prompt, tier="reasoning")
            
            cleaned_json = ai_response.replace("```json", "").replace("```", "").strip()
            report_data = json.loads(cleaned_json)
            
        except Exception as e:
            print(f"⚠️ [OSS Research Team Error] Fallback triggered: {e}")
            report_data = {
                "category": category,
                "top_recommendations": ["Fallback Tool A", "Fallback Tool B"],
                "best_choice": "Fallback Tool A",
                "reasoning": f"เกิดข้อผิดพลาดระหว่างประมวลผลระบบดึงข้อมูลอัตโนมัติ ({str(e)})",
                "free_tier_notes": "โปรดตรวจสอบการเชื่อมต่อ API อีกครั้ง"
            }

        research_entry = {
            "workflow_type": "oss_research_team",
            "category": category,
            "timestamp": dt.datetime.now().isoformat(),
            "status": "completed",
            "result": report_data
        }

        # บันทึกรายงานผลการวิจัยลงคลังความจำหลังบ้าน (00_memory)
        try:
            data = json.loads(self.research_path.read_text(encoding="utf-8"))
            data["reports"].append(research_entry)
            data["last_updated"] = dt.datetime.now().isoformat()
            data["total_reports"] = len(data["reports"])
            self.research_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"💾 [OSS Research Team] Report successfully logged to memory.")
        except Exception as e:
            print(f"⚠️ [Memory Log Error] Cannot save report: {e}")

        print(f"✅ [OSS Research Team] Completed research process for '{category}'")
        return research_entry

# ประกาศตัวแปร instance ให้ตรงกับชื่อที่ลงทะเบียนไว้ใน entry_point ของ JSON Registry
oss_research_team = OSSResearchTeam()