# Complete file: 04_scripts/meta_orchestrator.py
import json
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent
REGISTRY_PATH = ROOT / "00_memory" / "team_registry.json"
APPROVAL_QUEUE_PATH = ROOT / "00_memory" / "approval_queue.json"

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from shared_knowledge import shared_knowledge
# 🔗 นำเข้าผู้จัดการยูนิตปั๊มเงิน (Sub-Orchestrator) 
from growth_marketing_orchestrator import growth_marketing_orchestrator

BASE44_URL = "https://ai-agent-orchestrator-2vam.onrender.com"

class MetaOrchestrator:
    def __init__(self):
        self._ensure_registry_exists()
        self._ensure_approval_queue_exists()
        
    def _ensure_registry_exists(self):
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not REGISTRY_PATH.exists():
            default_registry = {
                "teams": {
                    "growth_marketing_bu": {
                        "name": "Autonomous Growth Marketing & Content BU",
                        "entry_point": "growth_marketing_orchestrator"
                    }
                }
            }
            REGISTRY_PATH.write_text(json.dumps(default_registry, indent=2, ensure_ascii=False), encoding="utf-8")

    def _ensure_approval_queue_exists(self):
        APPROVAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not APPROVAL_QUEUE_PATH.exists():
            APPROVAL_QUEUE_PATH.write_text(json.dumps({"pending": []}, indent=2, ensure_ascii=False), encoding="utf-8")

    async def route_and_execute(self, user_message: str, user_id: int):
        cleaned_msg = user_message.lower().replace("?", "").replace("!", "").strip()
        parts = cleaned_msg.split()
        
        if parts and (parts[0] == "approve" or parts[0] == "reject"):
            action = parts[0]
            if len(parts) < 2 or not parts[1].isdigit():
                return self.list_pending_approvals()
            return await self.process_gatekeeper_decision(action, int(parts[1]))
            
        # 💰 ส่งงานเข้าท่อของยูนิตทำเงิน Growth Marketing BU
        marketing_keywords = ["หาเงิน", "marketing", "ขาย", "content", "คอนเทนต์", "ข้าวสาร", "affiliate", "ธุรกิจ", "โปรดัก", "สินค้า", "ไอเดีย", "online", "ออนไลน์"]
        if any(kw in cleaned_msg for kw in marketing_keywords):
            print(f"🎯 [Meta Orchestrator] ส่งต่อภารกิจทำเงินก้อนโตให้ Growth Marketing BU...")
            try:
                # 🧠 ส่งต่อโจทย์ให้ Sub-Orchestrator ไปสั่งลูกทีมและประยุกต์คลังความคิด ดร.แสงสุข
                bu_result = growth_marketing_orchestrator.generate_strategic_plan(user_message)
                
                secure_payload = {
                    "flag_status": "active",
                    "payload_data": {
                        "best_tools": bu_result["best_tools"],
                        "conclusion": bu_result["conclusion"]
                    }
                }
                return self.hold_for_master_approval("growth_marketing_bu", user_message, secure_payload)
            except Exception as e_bu:
                print(f"💥 [Critical Error at Meta Routing] ติดขัด: {e_bu}")
                return {"status": "success", "data": {"message": f"⚠️ ยูนิตทำเงินติดขัดหลังบ้าน: {str(e_bu)}"}}

        guide_message = (
            f"🤖 **AI Command Center (Multi-Orchestrator Engine)**\n\n"
            f"ระบบปรับโครงสร้างแยกผู้จัดการยูนิตเสร็จสิ้นแล้วครับนายท่าน!\n"
            f"👉 พิมพ์ทดสอบคำสั่งปั๊มเงิน: *'ขอไอเดียทำธุรกิจ ข้าวสาร ออนไลน์'* ได้เลยครับ\n"
            f"👉 หรือเปิดหน้าแดชบอร์ดหลัก: [เปิดหน้าเว็บ Base44]({BASE44_URL})"
        )
        return {"status": "success", "data": {"message": guide_message}}

    def list_pending_approvals(self) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        pending_list = queue.get("pending", [])
        if not pending_list or len(pending_list) == 0:
            return {"status": "success", "data": {"message": "✅ **[Gatekeeper Report]** ไม่มีแผนงานปั๊มเงินค้างรออนุมัติในระบบครับ"}}
            
        msg = "📋 **[รายการแผนงานปั๊มเงินที่ค้างรออนุมัติ]**\n\n"
        for item in pending_list:
            msg += f"🆔 **รหัส: {item['id']}** | ยูนิต: `{item['team_id']}`\n🔍 โจทย์: {item['topic']}\n────────────────\n"
        msg += "👉 พิมพ์ **`approve ตามด้วยรหัส`** เพื่อปล่อยข้อมูลครับ"
        return {"status": "success", "data": {"message": msg}}

    def hold_for_master_approval(self, team_id: str, topic: str, result_data: dict) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        req_id = len(queue.get("pending", [])) + 1
        inner_data = result_data.get("payload_data", {})
        
        new_request = {
            "id": req_id,
            "team_id": team_id,
            "topic": topic,
            "result": {
                "best_tools": inner_data.get("best_tools", []),
                "conclusion": inner_data.get("conclusion", "")
            }
        }
        
        if "pending" not in queue or not isinstance(queue["pending"], list):
            queue["pending"] = []
            
        queue["pending"].append(new_request)
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
        
        msg = (
            f"📡 **[คำร้องอนุมัติยุทธศาสตร์ธุรกิจโดย ดร.แสงสุข Framework]**\n\n"
            f"🆔 **รหัสอนุมัติ:** {req_id}\n"
            f"👤 **ผู้ดูแลยูนิต:** `growth_marketing_orchestrator`\n"
            f"🔍 **โจทย์วิจัย:** {topic}\n\n"
            f"{inner_data.get('conclusion', '')}\n\n"
            f"⚠️ *ระบบล็อกคิวพิจารณาไว้แล้ว*\n"
            f"👉 พิมพ์ **`approve {req_id}`** เพื่อส่งแผนงานพรีเมียมลงหน้าเว็บ **Base44**"
        )
        return {"status": "success", "data": {"message": msg}}

    async def process_gatekeeper_decision(self, action: str, req_id: int) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"status": "success", "data": {"message": "❌ ไม่พบฐานข้อมูล"}}

        pending_list = queue.get("pending", [])
        target_req = None
        for req in pending_list:
            if req.get("id") == req_id:
                target_req = req
                break

        if not target_req:
            return {"status": "success", "data": {"message": f"❌ ไม่พบรายการคำร้องรหัส #{req_id}"}}

        queue["pending"] = [r for r in pending_list if r.get("id") != req_id]
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

        if action == "approve":
            res_data = target_req.get("result", {})
            shared_knowledge.publish_insight(
                author_team=target_req.get("team_id", "unknown"), 
                topic=target_req.get("topic", "unknown"), 
                insight_data={
                    "best_tools": res_data.get("best_tools", []), 
                    "conclusion": res_data.get("conclusion", "")
                }
            )
            msg = (
                f"✅ **[APPROVED MASTERPIECE]** อนุมัติแผนงานรหัส #{req_id} แล้ว!\n"
                f"คลังความรู้ระดับพรีเมียมตามกรอบแนวคิด ดร.แสงสุข ได้รับการเผยแพร่สดเรียบร้อย\n\n"
                f"🔗 คลิกเข้าดูความละเอียด: [เปิดคลังข้อมูลหน้าเว็บ Base44]({BASE44_URL})"
            )
            return {
                "status": "success", 
                "data": {
                    "message": msg,
                    "inline_buttons": [{"text": "🌐 Go to Base44 Web Portal", "url": BASE44_URL}]
                }
            }
        else:
            return {"status": "success", "data": {"message": f"❌ ปัดตกรหัส #{req_id} เรียบร้อยครับ"}}

meta_orchestrator = MetaOrchestrator()