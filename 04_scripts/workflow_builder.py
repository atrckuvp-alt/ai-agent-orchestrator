import json
from pathlib import Path
import datetime as dt
import sys
import asyncio
import importlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "04_scripts"))

from team_manager import team_manager
from meta_orchestrator import meta_orchestrator

async def execute_user_objective(objective: str, user_id: int = 7238952711):
    """
    [DYNAMIC PIPELINE FIXED] ฟังก์ชันหลักรับงานจากบอทมาจัดสรรทีมปฏิบัติการ
    แก้ไข: รองรับพารามิเตอร์ user_id เพื่อส่งต่อสัญญาณกลับหา Telegram สำเร็จ
    """
    workflow_id = f"wf_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"🎬 [Workflow Builder] Processing Objective for User {user_id} | Workflow: {workflow_id}")

    try:
        # 1. ยิงหา Meta Orchestrator เพื่อเลือกทีมย่อย
        routing_result = await meta_orchestrator.route_objective(objective, user_id=user_id)
        assigned_team = routing_result.get("team", "infrastructure_team")
        routing_reason = routing_result.get("reason", "วิเคราะห์โดยระบบอัจฉริยะ")

        # 2. ค้นหาไฟล์ประวัติสมุดโทรศัพท์ Registry เพื่อตรวจสอบโค้ดปลายทาง
        registry_path = ROOT / "00_memory" / "team_registry.json"
        if not registry_path.exists():
            raise FileNotFoundError(f"❌ ไม่พบไฟล์ระบบทีมที่ {registry_path}")
            
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        team_info = registry.get("teams", {}).get(assigned_team)
        
        if not team_info:
            raise ValueError(f"❌ ทีม '{assigned_team}' ไม่มีชื่ออยู่ในไฟล์ระบบ")

        entry_point_str = team_info.get("entry_point")

        # 3. บันทึกข้อมูลคลังความจำแอดวานซ์
        team_config = {
            "workflow_id": workflow_id,
            "team_type": assigned_team,
            "objective": objective,
            "routing_reason": routing_reason,
            "status": "active",
            "timestamp": dt.datetime.now().isoformat(),
            "entry_point": entry_point_str
        }
        team_manager.save_team(workflow_id, team_config)

        # 4. 🚀 [DYNAMIC INJECTION] ปลุกสมองทีมปฏิบัติการย่อยเบื้องหลัง
        module_path, instance_name = entry_point_str.split(":")
        team_module = importlib.import_module(module_path)
        team_instance = getattr(team_module, instance_name)

        # สั่งยิงโค้ดทำงานเบื้องหลัง Async ทันที พร้อมแนบไอดีเจ้าของคำสั่งไปด้วย
        if hasattr(team_instance, "research_open_source"):
            print(f"⚙️ [Dynamic Launch] Triggering {assigned_team} research task backend...")
            asyncio.create_task(team_instance.research_open_source(objective, user_id=user_id))

        report = f"""
✅ **Dynamic Workflow จัดตั้งทีมสำเร็จ!**

**Workflow ID:** `{workflow_id}`
**Objective:** {objective}
**Assigned Team:** `{team_info.get('name')}`
**Strategy Reason:** _{routing_reason}_

---
🤖 *ระบบย้ายเข้าสู่ท่อส่งงาน Dynamic สมบูรณ์แบบแล้ว กำลังเร่งจัดทำรายงานวิจัยส่งกลับเข้าแชทนี้ทันทีครับ!*
        """
        return {"success": True, "message": report.strip(), "workflow_id": workflow_id}

    except Exception as e:
        error_msg = f"❌ Dynamic Workflow พังทลายระหว่างส่งต่อพารามิเตอร์\nError: {str(e)}"
        print(f"🚨 [Workflow Builder Error]: {error_msg}")
        return {"success": False, "message": error_msg}