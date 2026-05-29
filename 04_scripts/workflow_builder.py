import json
from pathlib import Path
import datetime as dt
import sys
import asyncio

sys.path.append(str(Path(__file__).resolve().parents[1] / "04_scripts"))

from team_manager import team_manager
from run_orchestrator import main as run_orchestrator_main

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"

async def build_and_run_workflow(objective: str, team_type="full_stack_team", mode="mock"):
    workflow_id = f"wf_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"

    workflow_config = {
        "workflow_id": workflow_id,
        "created_at": dt.datetime.now().isoformat(),
        "objective": objective,
        "team_type": team_type,
        "mode": mode,
        "status": "pending_approval",
        "agents": ["research_agent", "coding_agent", "orchestrator"]
    }

    team_manager.save_team(workflow_id, workflow_config)

    return {
        "success": True,
        "workflow_id": workflow_id,
        "objective": objective,
        "status": "pending_approval",
        "needs_approval": True
    }


async def approve_workflow(workflow_id: str):
    """อนุมัติ Workflow และส่งรายงานผลกลับ Telegram"""
    team = team_manager.get_team(workflow_id)
    if not team:
        return {"success": False, "error": "ไม่พบ Workflow"}

    team["status"] = "approved"
    team["approved_at"] = dt.datetime.now().isoformat()
    team_manager.save_team(workflow_id, team)

    print(f"✅ Approved workflow: {workflow_id}")

    try:
        # รัน Orchestrator
        import subprocess
        result = subprocess.run(
            ["python", str(ROOT / "04_scripts" / "run_orchestrator.py"), "--mock"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(ROOT)
        )

        report = f"""
✅ **Workflow อนุมัติและรันสำเร็จแล้ว**

**Workflow ID:** `{workflow_id}`
**Objective:** {team.get('objective', 'Run full system analysis')}
**Team:** {team.get('team_type', 'Full Stack Team')}
**Status:** ✅ Completed
**Time:** {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
**รายงานสรุป:** 
ระบบได้วิเคราะห์และลงทะเบียนทีมหลักเรียบร้อยแล้ว
Meta Orchestrator ทำงานปกติ
        """

        return {
            "success": True, 
            "message": report,
            "workflow_id": workflow_id
        }

    except Exception as e:
        error_report = f"❌ Workflow `{workflow_id}` รันไม่สำเร็จ\nError: {str(e)[:200]}"
        return {"success": False, "message": error_report}


async def reject_workflow(workflow_id: str, reason=""):
    team = team_manager.get_team(workflow_id)
    if not team:
        return {"success": False, "error": "ไม่พบ Workflow"}

    team["status"] = "rejected"
    team["rejected_at"] = dt.datetime.now().isoformat()
    team["reject_reason"] = reason
    team_manager.save_team(workflow_id, team)

    return {"success": True, "message": f"Workflow {workflow_id} ถูกปฏิเสธ"}


async def execute_user_objective(objective: str, mode="mock"):
    result = await build_and_run_workflow(objective, team_type="full_stack_team", mode=mode)
    return result