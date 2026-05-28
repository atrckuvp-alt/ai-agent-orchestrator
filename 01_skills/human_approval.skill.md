# Human Approval Skill

## Mission
Control the final replacement decision.

## Allowed Human Decisions
- APPROVE
- REJECT
- TEST_FIRST

## If APPROVE
Update:
- `00_memory/current_stack.json`
- `00_memory/evaluation_history.json`
- `00_memory/model_registry.json`

## If REJECT
Keep current stack.
Record reason if available.

## If TEST_FIRST
Mark candidate as testing, not active.
