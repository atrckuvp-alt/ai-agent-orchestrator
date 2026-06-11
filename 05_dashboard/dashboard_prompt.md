Act as an Expert Frontend Developer. Please build a React/Tailwind dashboard application called "AI Model Research Team Command Center (Base44 V2)". 

This application must connect directly to my existing Supabase project and communicate with my external FastAPI backend for critical actions.

### 1. Database Integration (Supabase)
Assume the following tables already exist in Supabase. You need to fetch and display data from them using the Supabase JS client:
- `models`: (id, model_name, provider, category, open_source_status, free_tier_status, strengths, weaknesses, total_score, status, created_at)
- `evaluation_runs`: (id, run_id, report_path, recommendations, created_at)
- `approval_requests`: (id, request_id, category, old_model, new_model, reason, human_decision, created_at, decision_at)

### 2. Dashboard Layout & Sidebar
Create a persistent sidebar navigation with the following pages:
1. **Current Stack:** Display a health check widget and the currently active model.
2. **Candidate Models:** Display models where `status = 'candidate'`. Include filter buttons for categories (e.g., 'coding_analysis', 'research_reasoning'). Show "Strengths" and "Weaknesses" as nice UI tags or chips.
3. **Evaluation Runs:** A table showing benchmark results (Sandbox Benchmarks).
4. **Approval Queue:** Display pending approval requests. **CRITICAL WARNING UI:** Add a highly visible banner stating "No model replacement will occur before human approval."
5. **Decision History:** A table showing past approved/rejected requests.

### 3. Action Buttons & FastAPI Webhook Integration
In the "Approval Queue" or "Candidate Models" page, implement the following action buttons for each candidate. When clicked, show a loading state to prevent double-clicks:

- **APPROVE Button (Green):**
  When clicked, perform two actions sequentially:
  1. Make a POST request to: `https://ai-agent-orchestrator-2vam.onrender.com/api/v1/ai-research/approve-with-trace`
     Headers: 
     - `Content-Type: application/json`
     - `X-API-KEY: base44_core_v2_x89aF3kL9pQ2mZ5r`
     Body: `{ "request_id": "<generate_uuid_or_use_request_id>", "new_model": "<model_name>", "old_model": "<fetch_current_model_if_possible>" }`
  2. If the API returns success, update the Supabase `approval_requests` table to set `human_decision = 'APPROVED'` and `decision_at = NOW()`.

- **REJECT Button (Red):**
  Update the Supabase `approval_requests` table to set `human_decision = 'REJECTED'` and `decision_at = NOW()`. Do not call the external API.

- **EMERGENCY ROLLBACK Button (Orange/Warning - Place in Current Stack or Decision History):**
  Make a POST request to: `https://ai-agent-orchestrator-2vam.onrender.com/api/v1/ai-research/emergency-rollback`
  Headers:
  - `Content-Type: application/json`
  - `X-API-KEY: base44_core_v2_x89aF3kL9pQ2mZ5r`
  Body: `{ "request_id": "<provide_last_request_id_to_rollback>" }`
  Show a success toast if the rollback is successful.

Please use modern UI components (like Shadcn UI if available), score cards for the best models, and ensure the state updates dynamically. Ask me for the Supabase URL and Anon Key once you are ready to set up the connection.