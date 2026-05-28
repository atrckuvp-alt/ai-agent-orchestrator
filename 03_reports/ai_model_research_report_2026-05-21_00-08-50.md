# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-21T00:08:50

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
{"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"qwen/qwen3-next-80b-a3b-instruct:free is temporarily rate-limited upstream. Please retry shortly, or add your own key to accumulate your rate limits: https://openrouter.ai/settings/integrations","provider_name":"Venice","is_byok":false,"retry_after_seconds":25,"retry_after_seconds_raw":25}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### research_review
```text
**Recommendation:** **REJECT** (for now – none of the candidates have proven free‑tier access or verified open‑source licensing, and all benchmark runs failed with rate‑limit errors.)

---

## Why none of the three should be moved to production yet

| Candidate | Strengths | Weaknesses | Risks | Verdict |
|-----------|-----------|------------|-------|---------|
| **Baidu Qianfan: CoBuddy (free)** | – Live model on OpenRouter<br>– API‑accessible | – License undefined (must verify it is truly open‑source)<br>– Free‑tier status unknown<br>– Benchmark failed (rate‑limit 0/50) | – Provider could shut the model off or change limits without notice<br>– Possible legal exposure if the license is restrictive | **Reject / Test only after verification** |
| **NVIDIA: Nemotron 3 Nano Omni (free)** | – Same practical availability as above | – Same license‑verification gap<br>– Same free‑tier uncertainty<br>– Same rate‑limit block | – Same provider‑rate‑limit volatility risk | **Reject / Test only after verification** |
| **Poolside: Laguna XS.2 (free)** | – Same as above | – Same as above | – Same as above | **Reject / Test only after verification** |

### Common Issues Across All Candidates
1. **No Verified Open‑Source License** – The “verify exact license” flag means we cannot be sure they meet the open‑source preference or that downstream use is unrestricted.
2. **Free‑Tier Availability Unclear** – All three hit a `Rate limit exceeded: free‑models‑per‑day` error, indicating either the free quota is exhausted or the model is not truly free for ongoing use.
3. **Zero Benchmark Score** – Without successful benchmark results we have no evidence of reasoning quality, speed, or token‑cost efficiency.
4. **Provider Dependence** – All are hosted via OpenRouter; any change in the provider’s policies, pricing, or model deprecation would directly affect stability.

### Potential Next Steps (if a human still wants to explore)
1. **Verify Licensing** – Check the model repositories (e.g., Baidu’s model hub, NVIDIA’s NeMo, Poolside’s GitHub) for an explicit OSI‑approved license (Apache‑2.0, MIT, LGPL, etc.).
2. **Confirm Free‑Tier Terms** – Contact OpenRouter support or consult their documentation to see the exact daily quota and whether it can be increased without cost.
3. **Run a Controlled Benchmark** – After licensing and quota are cleared, run a small, reproducible reasoning benchmark (e.g., MATH or GSM8K) to get a real quality score.
4. **Evaluate Migration Difficulty** – Since all are “medium”, plan for potential replacement with a proven open‑source alternative (e.g., Llama 3‑8B‑Instruct) if any of these fail.

Until those checks are completed, moving any of these models into production would be premature and could expose the project to legal, reliability, and cost‑overrun risks. Therefore, **human approval is required to initiate further testing; otherwise, reject for now**.
```

### final_review
```text
**1. Coding recommendation**  
- **Result:** Failure – the coding agent could not retrieve a model response (HTTP 429 rate‑limit from the free Qwen 3‑Next‑80B endpoint).  
- **Implication:** No code‑generation capability demonstrated; the selected free tier is currently unavailable for development work.  

**2. Research recommendation**  
- **Result:** The research agent already concluded **REJECT** for all three candidates (Baidu Qianfan CoBuddy, NVIDIA Nemotron 3 Nano Omni, Poolside Laguna XS.2).  
- **Reasoning:**  
  - No verified open‑source license (cannot guarantee compliance).  
  - Free‑tier access is either exhausted or not clearly defined (rate‑limit errors).  
  - Benchmark runs failed, yielding no quality metrics.  
  - All models depend on a single provider (OpenRouter), introducing reliability and policy‑change risk.

**3. Risks**  
| Risk Category | Description |
|---------------|-------------|
| **Legal / Licensing** | Unclear OSI‑approved licenses could expose the project to copyright or usage restrictions. |
| **Reliability / Availability** | Rate‑limit (429) indicates the free tier cannot sustain the required request volume; provider may throttle or discontinue the model without notice. |
| **Performance Unknown** | No benchmark data → cannot assess reasoning quality, latency, or token cost. |
| **Vendor Lock‑in** | All models are hosted via OpenRouter; any change in pricing or terms directly affects the pipeline. |
| **Operational Cost Surprise** | If free quota is exceeded, the service may auto‑switch to a paid tier, incurring unexpected expenses. |

**4. Final decision suggestion**  
**TEST_FIRST** – Before any production deployment, the team should:

1. **Verify licensing** for each model (look for an explicit Apache‑2.0, MIT, LGPL, etc.).  
2. **Confirm free‑tier limits** with OpenRouter or obtain a personal API key to bypass shared quota.  
3. **Run a small benchmark** (e.g., GSM8K, MATH) once licensing and quota are clarified.  

If any of these steps fail, the appropriate action is to **REJECT** the candidates and consider proven open‑source alternatives (e.g., Llama 3‑8B‑Instruct, Mistral‑7B‑Instruct). Until those verifications are completed, do not move to production.
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
{"error":{"message":"Provider returned error","code":429,"metadata":{"raw":"qwen/qwen3-next-80b-a3b-instruct:free is temporarily rate-limited upstream. Please retry shortly, or add your own key to accumulate your rate limits: https://openrouter.ai/settings/integrations","provider_name":"Venice","is_byok":false,"retry_after_seconds":25,"retry_after_seconds_raw":25}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### research_review
```text
**Recommendation:** **REJECT** (for now – none of the candidates have proven free‑tier access or verified open‑source licensing, and all benchmark runs failed with rate‑limit errors.)

---

## Why none of the three should be moved to production yet

| Candidate | Strengths | Weaknesses | Risks | Verdict |
|-----------|-----------|------------|-------|---------|
| **Baidu Qianfan: CoBuddy (free)** | – Live model on OpenRouter<br>– API‑accessible | – License undefined (must verify it is truly open‑source)<br>– Free‑tier status unknown<br>– Benchmark failed (rate‑limit 0/50) | – Provider could shut the model off or change limits without notice<br>– Possible legal exposure if the license is restrictive | **Reject / Test only after verification** |
| **NVIDIA: Nemotron 3 Nano Omni (free)** | – Same practical availability as above | – Same license‑verification gap<br>– Same free‑tier uncertainty<br>– Same rate‑limit block | – Same provider‑rate‑limit volatility risk | **Reject / Test only after verification** |
| **Poolside: Laguna XS.2 (free)** | – Same as above | – Same as above | – Same as above | **Reject / Test only after verification** |

### Common Issues Across All Candidates
1. **No Verified Open‑Source License** – The “verify exact license” flag means we cannot be sure they meet the open‑source preference or that downstream use is unrestricted.
2. **Free‑Tier Availability Unclear** – All three hit a `Rate limit exceeded: free‑models‑per‑day` error, indicating either the free quota is exhausted or the model is not truly free for ongoing use.
3. **Zero Benchmark Score** – Without successful benchmark results we have no evidence of reasoning quality, speed, or token‑cost efficiency.
4. **Provider Dependence** – All are hosted via OpenRouter; any change in the provider’s policies, pricing, or model deprecation would directly affect stability.

### Potential Next Steps (if a human still wants to explore)
1. **Verify Licensing** – Check the model repositories (e.g., Baidu’s model hub, NVIDIA’s NeMo, Poolside’s GitHub) for an explicit OSI‑approved license (Apache‑2.0, MIT, LGPL, etc.).
2. **Confirm Free‑Tier Terms** – Contact OpenRouter support or consult their documentation to see the exact daily quota and whether it can be increased without cost.
3. **Run a Controlled Benchmark** – After licensing and quota are cleared, run a small, reproducible reasoning benchmark (e.g., MATH or GSM8K) to get a real quality score.
4. **Evaluate Migration Difficulty** – Since all are “medium”, plan for potential replacement with a proven open‑source alternative (e.g., Llama 3‑8B‑Instruct) if any of these fail.

Until those checks are completed, moving any of these models into production would be premature and could expose the project to legal, reliability, and cost‑overrun risks. Therefore, **human approval is required to initiate further testing; otherwise, reject for now**.
```

### final_review
```text
**1. Coding recommendation**  
- **Result:** Failure – the coding agent could not retrieve a model response (HTTP 429 rate‑limit from the free Qwen 3‑Next‑80B endpoint).  
- **Implication:** No code‑generation capability demonstrated; the selected free tier is currently unavailable for development work.  

**2. Research recommendation**  
- **Result:** The research agent already concluded **REJECT** for all three candidates (Baidu Qianfan CoBuddy, NVIDIA Nemotron 3 Nano Omni, Poolside Laguna XS.2).  
- **Reasoning:**  
  - No verified open‑source license (cannot guarantee compliance).  
  - Free‑tier access is either exhausted or not clearly defined (rate‑limit errors).  
  - Benchmark runs failed, yielding no quality metrics.  
  - All models depend on a single provider (OpenRouter), introducing reliability and policy‑change risk.

**3. Risks**  
| Risk Category | Description |
|---------------|-------------|
| **Legal / Licensing** | Unclear OSI‑approved licenses could expose the project to copyright or usage restrictions. |
| **Reliability / Availability** | Rate‑limit (429) indicates the free tier cannot sustain the required request volume; provider may throttle or discontinue the model without notice. |
| **Performance Unknown** | No benchmark data → cannot assess reasoning quality, latency, or token cost. |
| **Vendor Lock‑in** | All models are hosted via OpenRouter; any change in pricing or terms directly affects the pipeline. |
| **Operational Cost Surprise** | If free quota is exceeded, the service may auto‑switch to a paid tier, incurring unexpected expenses. |

**4. Final decision suggestion**  
**TEST_FIRST** – Before any production deployment, the team should:

1. **Verify licensing** for each model (look for an explicit Apache‑2.0, MIT, LGPL, etc.).  
2. **Confirm free‑tier limits** with OpenRouter or obtain a personal API key to bypass shared quota.  
3. **Run a small benchmark** (e.g., GSM8K, MATH) once licensing and quota are clarified.  

If any of these steps fail, the appropriate action is to **REJECT** the candidates and consider proven open‑source alternatives (e.g., Llama 3‑8B‑Instruct, Mistral‑7B‑Instruct). Until those verifications are completed, do not move to production.
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
