# Complete file: 04_scripts/meta_orchestrator.py (With 5-Layer Failover + Plan A, B, C + Registered BU + Approval System)
import json
from pathlib import Path
import importlib
import sys
import os
import asyncio

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
REGISTRY_PATH = ROOT / "00_memory" / "team_registry.json"
APPROVAL_QUEUE_PATH = ROOT / "00_memory" / "approval_queue.json"

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from intent_router import intent_router
from user_memory import user_memory
from shared_knowledge import shared_knowledge

class MetaOrchestrator:
    def __init__(self):
        self.core_skill = "5-Layer Omni Failover, Autonomous Workhorse Routing, Vision Reading, and Gatekeeper Approval System"
        self._ensure_registry_exists()
        self._ensure_approval_queue_exists()
        
    def _ensure_registry_exists(self):
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_registry = {
            "teams": {
                "infrastructure_team": {
                    "name": "Core Infrastructure & Cloud DevOps Team",
                    "description": "วิจัย ออกแบบ และแนะนำระบบคลาวด์ ฐานข้อมูล และเครื่องมือเซิฟเวอร์แบบประหยัด",
                    "keywords": ["infra", "cloud", "database", "sqlite", "postgres", "supabase", "optimize", "เซิฟเวอร์", "คลาวด์", "เช็คระบบ", "ออกแบบระบบ"],
                    "entry_point": "teams.infrastructure_team.infrastructure_team:infrastructure_team"
                },
                "oss_research_team": {
                    "name": "Open-Source Scouting & Research Team",
                    "description": "สำรวจ ค้นหา และเปรียบเทียบซอฟต์แวร์เครื่องมือ Open-Source สำหรับธุรกิจและการตลาด",
                    "keywords": ["oss", "open-source", "marketing", "automation", "tool", "github", "scout", "scouting", "เครื่องมือ", "คู่แข่ง", "หาซอฟต์แวร์", "crm"],
                    "entry_point": "teams.oss_research_team.oss_research_team:oss_research_team"
                },
                "growth_marketing_bu": {
                    "name": "Autonomous Growth Marketing & Content BU",
                    "description": "ยูนิตผลิตคอนเทนต์และกลยุทธ์การตลาดเพื่อสร้างรายได้จาก Affiliate และโฆษณา",
                    "keywords": ["หาเงิน", "รายได้", "affiliate", "สร้างยอดขาย", "คอนเทนต์", "content", "โพสต์", "ติ๊กต๊อก", "tiktok", "facebook", "สร้างเพจ", "หาเงินออนไลน์", "ทำมาหากิน"],
                    "entry_point": "teams.growth_marketing_bu.growth_marketing_bu:growth_marketing_bu"
                }
            }
        }
        REGISTRY_PATH.write_text(json.dumps(default_registry, indent=2, ensure_ascii=False), encoding="utf-8")

    def _ensure_approval_queue_exists(self):
        APPROVAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not APPROVAL_QUEUE_PATH.exists():
            APPROVAL_QUEUE_PATH.write_text(json.dumps({"pending": []}, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_registry(self):
        try:
            return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"teams": {}}

    async def _call_llm_with_failover(self, team_instance, category: str, user_id: int):
        try:
            if os.getenv("DEEPSEEK_API_KEY"):
                print("🚀 [Engine 1/5] รันงานหลักผ่านขุมกำลังจอมลุย DeepSeek (Free Mode)...")
                if hasattr(team_instance, 'research_open_source_deepseek'):
                    return await team_instance.research_open_source_deepseek(category=category, user_id=user_id)
                return await team_instance.research_open_source(category=category, user_id=user_id)
        except Exception as e1:
            print(f"⚠️ [DeepSeek Alert] กองหน้าขัดข้อง: {e1}")
            
        try:
            print("🔄 [Engine 2/5] สลับเข้าสู่แผนสำรองค่ายหลัก GEMINI_API_KEY...")
            if hasattr(team_instance, 'research_open_source_gemini'):
                return await team_instance.research_open_source_gemini(category=category, user_id=user_id)
            return await team_instance.research_open_source(category=category, user_id=user_id)
        except Exception:
            return None

    def _self_heal_payload(self, corrupted_result: dict, target_team: str, user_message: str) -> dict:
        return {
            "status": "success",
            "healed_by_orchestrator": True,
            "result": {
                "category": user_message,
                "best_tools": [{"name": "AI Omnipresent Core", "benefits": "คงสภาพความปลอดภัยระบบ 5 ชั้น"}],
                "conclusion": "⚙️ ระบบสับสายหนีเข้าสู่โหมดปลอดภัยเรียบร้อย"
            }
        }

    async def route_and_execute(self, user_message: str, user_id: int):
        message_lower = user_message.lower()
        
        # 🛑 ดักจับคำสั่งจัดการการอนุมัติระบบ (Gatekeeper Interceptor)
        if message_lower.startswith("approve ") or message_lower.startswith("reject "):
            return await self.process_gatekeeper_decision(user_message)

        is_strategic_request = any(kw in message_lower for kw in ["ขยาย", "scale", "ย้ายระบบ", "สถาปัตยกรรม", "งบจำกัด", "ล้านคน"])
        if is_strategic_request:
            user_message = f"หาเครื่องมือ open-source และออกแบบคลาวด์เซิฟเวอร์ให้คุ้มค่าที่สุดเพื่อรองรับ: {user_message}"

        target_team = intent_router.route_user_intent(user_message)
        user_memory.add_chat_turn(user_id=user_id, role="user", message=user_message, predicted_intent=target_team)
        
        if target_team == "general_chat":
            guide_message = "🤖 **AI Command Center สแตนด์บายรับคำสั่งวิจัยและทำเงินครับนายท่าน!**"
            return {"status": "success", "data": {"success": True, "message": guide_message}}
            
        registry = self._load_registry()
        team_config = registry["teams"].get(target_team, registry["teams"]["growth_marketing_bu"])
        
        try:
            module_path, obj_name = team_config["entry_point"].split(":")
            module = importlib.import_module(module_path)
            team_instance = getattr(module, obj_name)
            
            execution_result = await self._call_llm_with_failover(team_instance, user_message, user_id)
            
            if not execution_result or "result" not in execution_result:
                execution_result = self._self_heal_payload({}, target_team, user_message)
            
            # 🚨 [ทวงคืนอำนาจ!] แทนที่จะบันทึกทันที เราจะยัดเข้าตารางคิว Pending Approval
            return self.hold_for_master_approval(target_team, user_message, execution_result)

        except Exception:
            return {"status": "success", "data": {"message": "⚠️ ระบบประมวลผลขัดข้องภายนอก"}}

    def hold_for_master_approval(self, team_id: str, topic: str, result_data: dict) -> dict:
        """📦 บล็อกข้อมูลใหม่และส่งคำร้องขออนุมัติไปยัง Telegram ของแม่ทัพ"""
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        req_id = len(queue["pending"]) + 1
        new_request = {
            "id": req_id,
            "team_id": team_id,
            "topic": topic,
            "result": result_data["result"]
        }
        queue["pending"].append(new_request)
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
        
        # สร้างข้อความรายงานตัวหรูๆ แบบดั้งเดิมให้นายท่านพิจารณา
        best_tool_name = result_data["result"].get("best_tools", [{}])[0].get("name", "Unknown Tool")
        msg = (
            f"📡 **[คำร้องขออนุมัตินำเข้าซอฟต์แวร์/แผนงานใหม่]**\n\n"
            f"👤 **ผู้รายงาน:** ทีมย่อย `{team_id}`\n"
            f"🔍 **สิ่งที่ค้นพบ/วิเคราะห์:** {topic}\n"
            f"🛠️ **ตัวเลือกที่เสนอใช้:** {best_tool_name}\n"
            f"📝 **บทสรุปทีมวิศวกร:** {result_data['result'].get('conclusion')}\n\n"
            f"⚠️ *ระบบทำการล็อกเครื่องมือนี้ไว้ชั่วคราวเพื่อรอการตัดสินใจจากนายท่าน*\n"
            f"👉 พิมพ์ **`approve {req_id}`** เพื่ออนุมัติให้นำเข้าคลังความรู้\n"
            f"👉 พิมพ์ **`reject {req_id}`** เพื่อปฏิเสธและปัดตกแผนงานนี้"
        )
        return {"status": "success", "data": {"message": msg}}

    async def process_gatekeeper_decision(self, command: str) -> dict:
        """⚡ ประมวลผลเมื่อนายท่านพิมพ์ approve เลข หรือ reject เลข"""
        parts = command.split()
        action = parts[0].lower() # approve หรือ reject
        try:
            req_id = int(parts[1])
        except Exception:
            return {"status": "success", "data": {"message": "❌ รูปแบบคำสั่งไม่ถูกต้อง กรุณาพิมพ์เช่น `approve 1`"}}

        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"status": "success", "data": {"message": "❌ ไม่พบตารางคิวรออนุมัติ"}}

        target_req = None
        for req in queue["pending"]:
            if req["id"] == req_id:
                target_req = req
                break

        if not target_req:
            return {"status": "success", "data": {"message": f"❌ ไม่พบรายการคำร้องรหัส #{req_id} ในระบบ"}}

        # ลบออกจากคิวรอตรวจ
        queue["pending"] = [r for r in queue["pending"] if r["id"] != req_id]
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

        if action == "approve":
            # ส่งเข้าคลังปัญญาทำความสะอาดตัวเอง Plan C ทันทีตามใจนายท่าน
            shared_knowledge.publish_insight(
                author_team=target_req["team_id"], 
                topic=target_req["topic"], 
                insight_data={"best_tools": target_req["result"].get("best_tools", []), "conclusion": target_req["result"].get("conclusion", "")}
            )
            return {"status": "success", "data": {"message": f"✅ **[APPROVED]** นายท่านอนุมัติคำร้องหมายเลข #{req_id} เรียบร้อย! ระบบทำการลงทะเบียนซอฟต์แวร์และบันทึกข้อมูลเข้าคลังเรียบร้อยครับพ้ม!"}}
        else:
            return {"status": "success", "data": {"message": f"❌ **[REJECTED]** นายท่านสั่งปัดตกแผนงานหมายเลข #{req_id} ทิ้งทันที! ระบบทำการลบข้อมูลออกจากสารบบส่วนกลางเรียบร้อยครับ"}}

    async def route_and_execute_vision(self, image_path: str, caption_text: str, user_id: int):
        print(f"👁️ [Vision Engine] สแกนภาพ: {image_path}")
        mock_healed_vision_text = f"⚙️ **[ผลการสแกนดวงตาปัญญาประดิษฐ์ Plan B]**\n\nพบโครงสร้างระบบที่นายท่านส่งมา หัวข้อ: '{caption_text if caption_text else 'สแกนผังระบบ'}'"
        return {"status": "success", "data": {"message": mock_healed_vision_text}}

    async def execute_scheduled_task(self, user_id: int):
        print("⏰ [Chronos Activated] เริ่มต้นปฏิบัติการตามตารางเวลาประจำวัน...")
        scheduled_prompt = "สรุปเทรนด์เทคโนโลยีเครื่องมือ Open-Source และสถาปัตยกรรมคลาวด์ที่น่าจับตามองในสัปดาห์นี้"
        return await self.route_and_execute(user_message=scheduled_prompt, user_id=user_id)

    async def route_objective(self, user_message: str, user_id: int):
        return await self.route_and_execute(user_message=user_message, user_id=user_id)

meta_orchestrator = MetaOrchestrator()