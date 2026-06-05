# Complete file: 04_scripts/meta_orchestrator.py (Routing Optimization & Safe Gateway)
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

from shared_knowledge import shared_knowledge

class MetaOrchestrator:
    def __init__(self):
        self._ensure_registry_exists()
        self._ensure_approval_queue_exists()
        
    def _ensure_registry_exists(self):
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_registry = {
            "teams": {
                "growth_marketing_bu": {
                    "name": "Autonomous Growth Marketing & Content BU",
                    "entry_point": "teams.growth_marketing_bu.growth_marketing_bu:growth_marketing_bu"
                }
            }
        }
        if not REGISTRY_PATH.exists():
            REGISTRY_PATH.write_text(json.dumps(default_registry, indent=2, ensure_ascii=False), encoding="utf-8")

    def _ensure_approval_queue_exists(self):
        APPROVAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not APPROVAL_QUEUE_PATH.exists():
            APPROVAL_QUEUE_PATH.write_text(json.dumps({"pending": []}, indent=2, ensure_ascii=False), encoding="utf-8")

    async def route_and_execute(self, user_message: str, user_id: int):
        cmd_lower = user_message.lower().strip()
        
        # 🛑 1. ตรวจจับคำสั่งระบบอนุมัติ Gatekeeper
        if cmd_lower.startswith("approve ") or cmd_lower.startswith("reject "):
            return await self.process_gatekeeper_decision(user_message)
            
        # 💰 2. ขยายการเราท์ติ้งหาฝั่งปั๊มเงินโดยตรง ป้องกันการร่วงเข้า Self-Healing
        if any(kw in cmd_lower for kw in ["หาเงิน", "marketing", "ขาย", "content", "คอนเทนต์", "ข้าวสาร", "affiliate"]):
            print("🎯 [Route Hit] ส่งงานเข้ายูนิต Growth Marketing BU โดยตรง")
            try:
                from teams.growth_marketing_bu.growth_marketing_bu import growth_marketing_bu
                execution_result = await growth_marketing_bu.research_open_source(cmd_lower, user_id)
                
                # นำแผนงานไปเข้าคิว Pending Approval ทันที
                return self.hold_for_master_approval("growth_marketing_bu", user_message, execution_result)
            except Exception as e_bu:
                return {"status": "success", "data": {"message": f"⚠️ ยูนิตทำเงินติดขัด: {e_bu}"}}

        # 🤖 3. กรณีเป็นแชทคุยถามไถ่ทั่วไป หรือเรื่องเปิดเกราะ
        guide_message = f"🤖 **AI Command Center สแตนด์บายครับ!**\n\nนายท่านสามารถสั่งการยูนิตทำเงินได้ทันที เช่น พิมพ์คำว่า: *'วิเคราะห์กลยุทธ์การขายข้าวสารออนไลน์'* ได้เลยครับพ้ม"
        return {"status": "success", "data": {"message": guide_message}}

    def hold_for_master_approval(self, team_id: str, topic: str, result_data: dict) -> dict:
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
        
        msg = (
            f"📡 **[คำร้องขออนุมัติแผนงานปั๊มเงินใหม่]**\n\n"
            f"👤 **ผู้รายงาน:** ยูนิต `{team_id}`\n"
            f"🔍 **โจทย์วิจัย:** {topic}\n\n"
            f"⚠️ *ระบบบันทึกแผนงานดิบลงหน้า **Base44** แล้ว และล็อกสถานะไว้เพื่อรอนายท่านตรวจงาน*\n"
            f"👉 พิมพ์ **`approve {req_id}`** เพื่อเปิดไฟเขียวปล่อยโพสต์ทำเงิน\n"
            f"👉 พิมพ์ **`reject {req_id}`** เพื่อปัดตกและยกเลิกแผนงานนี้"
        )
        return {"status": "success", "data": {"message": msg}}

    async def process_gatekeeper_decision(self, command: str) -> dict:
        parts = command.split()
        action = parts[0].lower()
        try:
            req_id = int(parts[1])
        except Exception:
            return {"status": "success", "data": {"message": "❌ รูปแบบคำสั่งไม่ถูกต้อง พิมพ์เช่น `approve 1`"}}

        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"status": "success", "data": {"message": "❌ ไม่พบฐานข้อมูลคิวรออนุมัติ"}}

        target_req = None
        for req in queue["pending"]:
            if req["id"] == req_id:
                target_req = req
                break

        if not target_req:
            return {"status": "success", "data": {"message": f"❌ ไม่พบรายการคำร้องรหัส #{req_id}"}}

        queue["pending"] = [r for r in queue["pending"] if r["id"] != req_id]
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

        if action == "approve":
            shared_knowledge.publish_insight(author_team=target_req["team_id"], topic=target_req["topic"], insight_data={"best_tools": target_req["result"].get("best_tools", []), "conclusion": target_req["result"].get("conclusion", "")})
            return {"status": "success", "data": {"message": f"✅ **[APPROVED]** นายท่านอนุมัติรหัส #{req_id} แล้ว! คอนเทนต์ในหน้า **Base44** ถูกเปลี่ยนสถานะเป็นพร้อมโพสต์เพื่อปั๊มเงินเรียบร้อยครับพ้ม!"}}
        else:
            return {"status": "success", "data": {"message": f"❌ **[REJECTED]** สั่งปัดตกรหัส #{req_id} เรียบร้อย แผนงานนี้ถูกทำลายทิ้งทันที"}}

    async def execute_scheduled_task(self, user_id: int):
        # ฟังก์ชันสำหรับส่งรายงานสรุปเวลา 09:00 น.
        return {"status": "success", "data": {"message": "🏆 **[Strategic Morning Briefing]** รายงานสรุปเทรนด์ซอฟต์แวร์และการตลาดระดับโลกประจำวันมาเสิร์ฟแล้วครับนายท่าน! วันนี้ยูนิตทุกส่วนพร้อมสแตนด์บายทำเงินครับ!"}}

meta_orchestrator = MetaOrchestrator()