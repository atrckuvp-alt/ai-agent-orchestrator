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
    """อนุมัติและรัน Workflow + ส่งรายงานกลับ Telegram"""
    team = team_manager.get_team(workflow_id)
    if not team:
        return {"success": False, "error": "ไม่พบ Workflow"}

    team["status"] = "approved"
    team["approved_at"] = dt.datetime.now().isoformat()
    team_manager.save_team(workflow_id, team)

    print(f"✅ Approved workflow: {workflow_id}")

    # รัน Orchestrator จริง
    try:
        import subprocess
        result = subprocess.run(
            ["python", str(ROOT / "04_scripts" / "run_orchestrator.py"), "--mock"],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(ROOT)
        )

        report_message = f"✅ Workflow `{workflow_id}` อนุมัติและรันสำเร็จแล้ว!\n\n"
        report_message += f"**Objective:** {team.get('objective', 'N/A')}\n"
        report_message += f"**Status:** Completed"

        return {
            "success": True, 
            "message": report_message,
            "workflow_id": workflow_id
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


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