# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-21T00:01:11

## Executive Summary

This MVP report compares candidate AI models/tools against the current baseline. No replacement is performed automatically.

## Category: coding_analysis

| Rank | Model | Provider | Score | Recommendation Style |
|---:|---|---|---:|---|
| 1 | Qwen: Qwen3 Coder 480B A35B (free) | OpenRouter | 84 | Candidate |
| 2 | Pareto Code Router | OpenRouter | 79 | Candidate |
| 3 | Kwaipilot: KAT-Coder-Pro V2 | OpenRouter | 79 | Candidate |

### Qwen: Qwen3 Coder 480B A35B (free)
- Provider: OpenRouter
- Open-source status: verify exact license
- Free-tier/API status: verify current free-tier
- Best use case: dynamic evaluation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
### Pareto Code Router
- Provider: OpenRouter
- Open-source status: verify exact license
- Free-tier/API status: verify current free-tier
- Best use case: dynamic evaluation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
### Kwaipilot: KAT-Coder-Pro V2
- Provider: OpenRouter
- Open-source status: verify exact license
- Free-tier/API status: verify current free-tier
- Best use case: dynamic evaluation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
- Benchmark score: 0
- Benchmark failed:
```text
{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 65536 tokens, but can only afford 33333. To increase, visit https://openrouter.ai/settings/credits and upgrade to a paid account","code":402,"metadata":{"provider_name":null}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```
- Strengths:
  - live discovered model
  - available via API
  - candidate for testing
- Weaknesses:
  - license must be verified
  - availability may change
  - needs benchmark testing

## Agent Team Review

### coding_review
```text
'choices'
```

### research_review
```text
'choices'
```

### final_review
```text
**1. Coding recommendation**  
- The coding agent failed to generate a response (error: *'choices'*). No usable code or evaluation is available.  

**2. Research recommendation**  
- The research agent also failed to produce output (error: *'choices'*). No analysis of alternative models or data has been delivered.  

**3. Risks**  
- **Model reliability:** Repeated “'choices'” errors suggest the selected `openrouter/free` endpoint is mis‑configured, unstable, or mismatched with the expected API schema. Continuing to rely on it could cause silent failures in downstream pipelines.  
- **Deployment impact:** Without validated code or research, integrating this model may break existing services or introduce latency/incorrect behavior.  
- **Security / compliance:** Unchecked failures may hide larger issues (e.g., malformed requests that could expose API keys).  

**4. Final decision suggestion**  
**KEEP_CURRENT** – retain the existing, stable model(s) until the failure is investigated and resolved.  

*Next steps (human‑approved):*  
1. Verify the OpenRouter API endpoint and request format (ensure the response includes a `choices` list).  
2. Run a minimal sanity test to confirm the model can return a valid completion.  
3. Only after successful verification should the coding and research agents be re‑run.
```

## Category: research_reasoning

| Rank | Model | Provider | Score | Recommendation Style |
|---:|---|---|---:|---|
| 1 | Baidu Qianfan: CoBuddy (free) | OpenRouter | 84 | Candidate |
| 2 | NVIDIA: Nemotron 3 Nano Omni (free) | OpenRouter | 84 | Candidate |
| 3 | Poolside: Laguna XS.2 (free) | OpenRouter | 84 | Candidate |

### Baidu Qianfan: CoBuddy (free)
- Provider: OpenRouter
- Open-source status: verify exact license
- Free-tier/API status: verify current free-tier
- Best use case: dynamic evaluation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
### NVIDIA: Nemotron 3 Nano Omni (free)
- Provider: OpenRouter
- Open-source status: verify exact license
- Free-tier/API status: verify current free-tier
- Best use case: dynamic evaluation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
### Poolside: Laguna XS.2 (free)
- Provider: OpenRouter
- Open-source status: verify exact license
- Free-tier/API status: verify current free-tier
- Best use case: dynamic evaluation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
- Benchmark score: 0
- Benchmark failed:
```text
{"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1779321600000"},"provider_name":null}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```
- Strengths:
  - live discovered model
  - available via API
  - candidate for testing
- Weaknesses:
  - license must be verified
  - availability may change
  - needs benchmark testing

## Agent Team Review

### coding_review
```text
'choices'
```

### research_review
```text
'choices'
```

### final_review
```text
**1. Coding recommendation**  
- The coding agent failed to generate a response (error: *'choices'*). No usable code or evaluation is available.  

**2. Research recommendation**  
- The research agent also failed to produce output (error: *'choices'*). No analysis of alternative models or data has been delivered.  

**3. Risks**  
- **Model reliability:** Repeated “'choices'” errors suggest the selected `openrouter/free` endpoint is mis‑configured, unstable, or mismatched with the expected API schema. Continuing to rely on it could cause silent failures in downstream pipelines.  
- **Deployment impact:** Without validated code or research, integrating this model may break existing services or introduce latency/incorrect behavior.  
- **Security / compliance:** Unchecked failures may hide larger issues (e.g., malformed requests that could expose API keys).  

**4. Final decision suggestion**  
**KEEP_CURRENT** – retain the existing, stable model(s) until the failure is investigated and resolved.  

*Next steps (human‑approved):*  
1. Verify the OpenRouter API endpoint and request format (ensure the response includes a `choices` list).  
2. Run a minimal sanity test to confirm the model can return a valid completion.  
3. Only after successful verification should the coding and research agents be re‑run.
```

## Final Recommendation

### coding_analysis
- Current baseline score: 70
- Best candidate: Qwen: Qwen3 Coder 480B A35B (free)
- Best candidate score: 84
- Improvement: 20.0%
- Decision: REPLACE_AFTER_APPROVAL

### research_reasoning
- Current baseline score: 70
- Best candidate: Baidu Qianfan: CoBuddy (free)
- Best candidate score: 84
- Improvement: 20.0%
- Decision: REPLACE_AFTER_APPROVAL

## Human Approval

Choose one:
- APPROVE
- REJECT
- TEST_FIRST

No system change should happen until human decision is recorded.
