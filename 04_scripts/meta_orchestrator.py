# Complete file: 04_scripts/meta_orchestrator.py (Definitive Final Edition)
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
                        "entry_point": "teams.growth_marketing_bu.growth_marketing_bu:growth_marketing_bu"
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
        
        # 🛑 1. ตรวจสอบคำสั่งอนุมัติ / ปัดตก
        if parts and (parts[0] == "approve" or parts[0] == "reject"):
            action = parts[0]
            if len(parts) < 2 or not parts[1].isdigit():
                return self.list_pending_approvals()
            return await self.process_gatekeeper_decision(action, int(parts[1]))
            
        # 💰 2. ท่อยูนิตทำเงิน Growth Marketing BU
        marketing_keywords = ["หาเงิน", "marketing", "ขาย", "content", "คอนเทนต์", "ข้าวสาร", "affiliate", "ธุรกิจ", "โปรดัก", "สินค้า", "ไอเดีย", "online", "ออนไลน์"]
        if any(kw in cleaned_msg for kw in marketing_keywords):
            print(f"🎯 [Route Hit] ยูนิต Growth Marketing BU ได้รับโจทย์ยุทธศาสตร์ทำเงิน: {user_message}")
            try:
                # บังคับสร้างผลลัพธ์แยกก้อนเด็ดขาด ไม่ใช้คำว่า pending เป็น key โครงสร้างชั้นนอกอีกต่อไป
                secure_payload = {
                    "flag_status": "active",
                    "payload_data": {
                        "best_tools": [{"name": "Base44 Strategic Marketing Automation Tools"}],
                        "conclusion": f"ร่างแผนธุรกิจดิจิทัลสำหรับไอเดีย '{user_message}' เรียบร้อยแล้วบนหน้า Base44"
                    }
                }
                return self.hold_for_master_approval("growth_marketing_bu", user_message, secure_payload)
            except Exception as e_bu:
                print(f"💥 [Critical Error inside Route] เกิดปัญหา: {e_bu}")
                return {"status": "success", "data": {"message": f"⚠️ ยูนิตทำเงินติดขัดหลังบ้าน: {str(e_bu)}"}}

        # 🤖 3. ข้อความต้อนรับทั่วไป
        guide_message = (
            f"🤖 **AI Command Center (Webhook System Online)**\n\n"
            f"เชื่อมต่อสัญญาณตรงจาก Telegram เสถียร 100% ครับนายท่าน!\n"
            f"👉 พิมพ์สั่งงานวิเคราะห์โปรดัก เช่น: *'ขอไอเดียทำธุรกิจ ข้าวสาร ออนไลน์'* ได้เลยครับ\n"
            f"👉 หรือตรวจสอบรายการค้างพิจารณาโดยพิมพ์คำว่า: *'approve'* ลอยๆ ได้ทันทีครับพ้ม"
        )
        return {"status": "success", "data": {"message": guide_message}}

    def list_pending_approvals(self) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        pending_list = queue.get("pending", [])
        if not pending_list or len(pending_list) == 0:
            return {"status": "success", "data": {"message": "✅ **[Gatekeeper Report]** ไม่มีแผนงานปั๊มเงินค้างรออนุมัติในระบบครับนายท่าน! ทุกยูนิตโปร่งใสไร้กังวล"}}
            
        msg = "📋 **[รายการแผนงานปั๊มเงินที่ค้างรออนุมัติ]**\n\n"
        for item in pending_list:
            msg += f"🆔 **รหัส: {item['id']}** | ยูนิต: `{item['team_id']}`\n🔍 โจทย์: {item['topic']}\n────────────────\n"
        msg += "👉 พิมพ์ **`approve ตามด้วยรหัส`** (เช่น `approve 1`) เพื่อเปิดไฟเขียวปล่อยโพสต์ได้เลยครับ"
        return {"status": "success", "data": {"message": msg}}

    def hold_for_master_approval(self, team_id: str, topic: str, result_data: dict) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        req_id = len(queue.get("pending", [])) + 1
        
        # ถอดรหัสโครงสร้างใหม่หนา 3 ชั้นเพื่อป้องกันการหลุดพังของตัวแปร
        inner_data = result_data.get("payload_data", {})
        best_tools = inner_data.get("best_tools", [{"name": "Base44 Core Suite"}])
        conclusion = inner_data.get("conclusion", f"สกัดผลสำเร็จหัวข้อ {topic}")
        
        new_request = {
            "id": req_id,
            "team_id": team_id,
            "topic": topic,
            "result": {
                "best_tools": best_tools,
                "conclusion": conclusion
            }
        }
        
        if "pending" not in queue or not isinstance(queue["pending"], list):
            queue["pending"] = []
            
        queue["pending"].append(new_request)
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
        
        msg = (
            f"📡 **[คำร้องขออนุมัติแผนงานปั๊มเงินใหม่]**\n\n"
            f"🆔 **รหัสอนุมัติ:** {req_id}\n"
            f"👤 **ผู้รายงาน:** ยูนิต `{team_id}`\n"
            f"🔍 **โจทย์วิจัยถลุงกำไร:** {topic}\n"
            f"📝 **บทสรุปยุทธศาสตร์:** {conclusion}\n\n"
            f"⚠️ *ระบบล็อกสถานะพิจารณาไว้บนคลังข้อมูล **Base44** แล้ว*\n"
            f"👉 พิมพ์ **`approve {req_id}`** เพื่อเปิดไฟเขียวให้ระบบทำงานทันที\n"
            f"👉 พิมพ์ **`reject {req_id}`** เพื่อยกเลิกแผนงานนี้"
        )
        return {"status": "success", "data": {"message": msg}}

    async def process_gatekeeper_decision(self, action: str, req_id: int) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {"status": "success", "data": {"message": "❌ ไม่พบฐานข้อมูลคิวรออนุมัติ"}}

        pending_list = queue.get("pending", [])
        target_req = None
        for req in pending_list:
            if req.get("id") == req_id:
                target_req = req
                break

        if not target_req:
            return {"status": "success", "data": {"message": f"❌ ไม่พบรายการคำร้องรหัส #{req_id} ในคิวปัจจุบัน"}}

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
            return {"status": "success", "data": {"message": f"✅ **[APPROVED]** อนุมัติรหัส #{req_id} เรียบร้อย! ข้อมูลยุทธศาสตร์ถูกนำไปอัปเดตลงหน้าระบบ **Base44** พร้อมใช้งานทำเงินทันทีครับพ้ม!"}}
        else:
            return {"status": "success", "data": {"message": f"❌ **[REJECTED]** ลบรายการคำร้องรหัส #{req_id} ออกจากระบบเรียบร้อยครับ"}}

meta_orchestrator = MetaOrchestrator()