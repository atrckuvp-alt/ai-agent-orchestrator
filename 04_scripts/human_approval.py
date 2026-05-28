"""
Approve or reject a pending model recommendation.

Examples:
    python 04_scripts/human_approval.py --request-id REQ-xxxx-coding_analysis --decision TEST_FIRST
    python 04_scripts/human_approval.py --request-id REQ-xxxx-coding_analysis --decision APPROVE
    python 04_scripts/human_approval.py --request-id REQ-xxxx-coding_analysis --decision REJECT
"""

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--decision", required=True, choices=["APPROVE", "REJECT", "TEST_FIRST"])
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    approval_path = MEMORY / "approval_queue.json"
    current_path = MEMORY / "current_stack.json"

    approval = load_json(approval_path)
    current = load_json(current_path)

    target = None
    for req in approval["approval_requests"]:
        if req["request_id"] == args.request_id:
            target = req
            break

    if not target:
        raise RuntimeError(f"Request not found: {args.request_id}")

    target["human_decision"] = args.decision
    target["human_note"] = args.note
    target["decision_at"] = dt.datetime.now().isoformat(timespec="seconds")

    runtime_path = MEMORY / "agent_runtime_config.json"
    runtime_config = load_json(runtime_path)

    if args.decision == "APPROVE":
        category = target["category"]
        current["categories"][category]["current_model"] = target["new_model"]
        current["categories"][category]["provider"] = "approved from MVP report"
        current["categories"][category]["reason_using"] = target.get(
            "reason_to_replace_or_test",
            target.get("decision_required", "Approved by human")
        )   
        current["categories"][category]["status"] = "active"
        current["categories"][category]["approved_by"] = "human"
        current["categories"][category]["approved_at"] = target["decision_at"]
        current["last_updated"] = target["decision_at"]

        # AUTO RUNTIME SWITCH

        if category == "coding_analysis":
            runtime_config["coding_agent"]["model"] = target.get(
                "model_id",
                target.get("new_model")
            )

        if category == "research_reasoning":
            runtime_config["research_agent"]["model"] = target.get(
                "model_id",
                target.get("new_model")
            )

    elif args.decision == "TEST_FIRST":
        target["status"] = "testing_only_not_active"

    elif args.decision == "REJECT":
        target["status"] = "rejected_keep_current"

    save_json(approval_path, approval)
    save_json(current_path, current)
    save_json(runtime_path, runtime_config)

    print(f"Decision recorded: {args.decision}")
    if args.decision == "APPROVE":
        print("Current stack updated.")

        print("Auto rerun orchestrator after approval...")

        subprocess.run(
            [
                "python",
                "04_scripts\\run_orchestrator.py",
                "--api",
                "openrouter"
            ],
            check=False
        )
    else:
        print("Current stack unchanged.")

if __name__ == "__main__":
    main()
