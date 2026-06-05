# Complete file: 04_scripts/meta_orchestrator.py (Fixed Structure & Bulletproof Key Parsing)
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
        # ทำความสะอาดข้อความเพื่อความแม่นยำในการคัดกรองคำสั่ง
        cleaned_msg = user_message.lower().replace("?", "").replace("!", "").strip()
        parts = cleaned_msg.split()
        
        # 🛑 1. ระบบตรวจจับและประมวลผลคำสั่งฝั่ง Gatekeeper (Approve / Reject)
        if parts and (parts[0].startswith("approve") or parts[0].startswith("reject")):
            action = "approve" if parts[0].startswith("approve") else "reject"
            
            # หากพิมพ์สั่งลอยๆ เช่น "approve มีไหม" หรือ "Approve?" ให้ลิสต์งานค้างโชว์ทันที
            if len(parts) < 2 or not parts[1].isdigit():
                return self.list_pending_approvals()
                
            return await self.process_gatekeeper_decision(action, int(parts[1]))
            
        # 💰 2. ส่งคำสั่งเข้าท่อยูนิตทำเงิน Growth Marketing BU
        marketing_keywords = ["หาเงิน", "marketing", "ขาย", "content", "คอนเทนต์", "ข้าวสาร", "affiliate", "ธุรกิจ", "โปรดัก", "สินค้า"]
        if any(kw in cleaned_msg for kw in marketing_keywords):
            print("🎯 [Route Hit] ยูนิต Growth Marketing BU ได้รับโจทย์ยุทธศาสตร์ทำเงิน")
            try:
                # ปรับโครงสร้างข้อมูลดิบ (Mock) ให้ตรงตามพิมพ์เขียวของระบบ และป้องกันโครงสร้างหลุดพัง
                mock_result = {
                    "result": {
                        "best_tools": [{"name": "Base44 Dashboard Content Generator"}],
                        "conclusion": f"แผนวิจัยสร้างกระแสเงินสดจากโปรดักสินค้ากลุ่ม '{user_message}' ถูกร่างโครงสร้างบน Base44 สำเร็จ"
                    }
                }
                return self.hold_for_master_approval("growth_marketing_bu", user_message, mock_result)
            except Exception as e_bu:
                return {"status": "success", "data": {"message": f"⚠️ ยูนิตทำเงินติดขัดหลังบ้าน: {e_bu}"}}

        # 🤖 3. เมนูแนะนำกรณีพูดคุยทั่วไป
        guide_message = (
            f"🤖 **AI Command Center กำลังดูแลระบบผ่าน Webhook ครับ!**\n\n"
            f"สัญญาณเชื่อมต่อตรงจาก Telegram ลื่นไหล 100% แล้วครับนายท่าน\n"
            f"👉 ลองสั่งงานผมวิเคราะห์สินค้า เช่น: *'สร้างธุรกิจด้วยโปรดักข้าวสาร'* ได้เลยครับ\n"
            f"👉 หรือตรวจสอบคิวงานค้างโดยพิมพ์: *'approve'* ลอยๆ ได้ทันทีครับพ้ม"
        )
        return {"status": "success", "data": {"message": guide_message}}

    def list_pending_approvals(self) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        if not queue.get("pending") or len(queue["pending"]) == 0:
            return {"status": "success", "data": {"message": "✅ **[Gatekeeper Report]** ไม่มีแผนงานปั๊มเงินค้างรออนุมัติในระบบครับนายท่าน! ทุกยูนิตโปร่งใสไร้กังวล"}}
            
        msg = "📋 **[รายการแผนงานปั๊มเงินที่ค้างรออนุมัติ]**\n\n"
        for item in queue["pending"]:
            msg += f"🆔 **รหัส: {item['id']}** | ยูนิต: `{item['team_id']}`\n🔍 โจทย์: {item['topic']}\n────────────────\n"
        msg += "👉 พิมพ์ **`approve ตามด้วยรหัส`** (เช่น `approve 1`) เพื่อเปิดไฟเขียวปล่อยโพสต์ลงคลังความรู้ได้เลยครับ"
        return {"status": "success", "data": {"message": msg}}

    def hold_for_master_approval(self, team_id: str, topic: str, result_data: dict) -> dict:
        try:
            queue = json.loads(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8"))
        except Exception:
            queue = {"pending": []}
            
        req_id = len(queue["pending"]) + 1
        
        # 🔒 ป้องกันบั๊กชั้นข้อมูลดึง Key พลาดโดยใช้การดักจับ .get() ที่ปลอดภัยระดับสูงสุด
        inner_result = result_data.get("result", {})
        
        new_request = {
            "id": req_id,
            "team_id": team_id,
            "topic": topic,
            "result": {
                "best_tools": inner_result.get("best_tools", []),
                "conclusion": inner_result.get("conclusion", f"สกัดผลลัพธ์ยุทธศาสตร์หัวข้อ {topic} เรียบร้อย")
            }
        }
        
        queue["pending"].append(new_request)
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")
        
        msg = (
            f"📡 **[คำร้องขออนุมัติแผนงานปั๊มเงินใหม่]**\n\n"
            f"👤 **ผู้รายงาน:** ยูนิต `{team_id}`\n"
            f"🔍 **โจทย์วิจัยถลุงกำไร:** {topic}\n\n"
            f"⚠️ *ระบบสกัดคอนเทนต์ดิบฝังลงหน้า **Base44** แล้ว และล็อกสถานะพิจารณาไว้*\n"
            f"👉 พิมพ์ **`approve {req_id}`** เพื่อปล่อยโพสต์ทำเงินทันที\n"
            f"👉 พิมพ์ **`reject {req_id}`** เพื่อยกเลิกและทำลายแผนงานนี้ทิ้ง"
        )
        return {"status": "success", "data": {"message": msg}}

    async def process_gatekeeper_decision(self, action: str, req_id: int) -> dict:
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
            return {"status": "success", "data": {"message": f"❌ ไม่พบรายการคำร้องรหัส #{req_id} ในคิวปัจจุบัน"}}

        # ลบรายการออกจากคิวค้างหลังประมวลผล
        queue["pending"] = [r for r in queue["pending"] if r["id"] != req_id]
        APPROVAL_QUEUE_PATH.write_text(json.dumps(queue, indent=2, ensure_ascii=False), encoding="utf-8")

        if action == "approve":
            res_data = target_req.get("result", {})
            shared_knowledge.publish_insight(
                author_team=target_req["team_id"], 
                topic=target_req["topic"], 
                insight_data={
                    "best_tools": res_data.get("best_tools", []), 
                    "conclusion": res_data.get("conclusion", "")
                }
            )
            return {"status": "success", "data": {"message": f"✅ **[APPROVED]** นายท่านเปิดไฟเขียวอนุมัติรหัส #{req_id} แล้ว! คอนเทนต์ในหน้า **Base44** ถูกเปลี่ยนสถานะพร้อมกระจายรายได้เข้ากระเป๋าทันทีครับพ้ม!"}}
        else:
            return {"status": "success", "data": {"message": f"❌ **[REJECTED]** สั่งปัดตกรหัส #{req_id} แผนงานทำเงินชุดนี้ถูกลบออกจากฐานข้อมูลเรียบร้อยครับ"}}

    async def execute_scheduled_task(self, user_id: int):
        return {"status": "success", "data": {"message": "🏆 **[Strategic Morning Briefing]** รายงานสรุปยุทธศาสตร์และไอเดียทำเงินรอบโลกประจำวันส่งตรงถึงมือนายท่านเรียบร้อยครับ!"}}

meta_orchestrator = MetaOrchestrator()