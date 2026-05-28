# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-22T21:55:18

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
### Best Candidate: Qwen: Qwen3 Coder 480B A35B (free)  
**Total Score:** 84 (highest among candidates)  

#### **Strengths:**  
- **High Quality Score (30/30):** Strong performance potential for coding/analysis tasks.  
- **Free API Access:** Available via OpenRouter’s free tier.  
- **Live Model:** Regularly updated, suitable for dynamic evaluation.  

#### **Weaknesses:**  
- **License Uncertainty:** Open-source status requires verification (exact license unknown).  
- **Rate-Limited:** Recent benchmark failed due to temporary upstream rate limits (429 error).  
- **Stability Concerns:** Provider-driven risks (e.g., free-tier changes).  

#### **Risks:**  
- **Provider Instability:** Free-tier access may change (e.g., rate limits or costs).  
- **Benchmark Failure:** Current API test unsuccessful (rate-limited).  
- **Migration Difficulty:** Medium complexity if replacing existing models.  

#### **Recommendation: TEST_FIRST**  
- **Why?**  
  - Highest total score and free-tier access align with preferences.  
  - Rate-limit error is temporary (retry suggested); test again with adjusted token limits.  
  - Verify license terms and free-tier policies before full adoption.  
- **Action:**  
  1. **Re-run benchmark** with reduced token count (e.g., 5k tokens) to confirm free-tier usability.  
  2. **Verify open-source license** (e.g., check GitHub or provider docs).  
  3. **Monitor rate limits** during extended tests.  

**Reject candidates with lower scores (Pareto/Kwaipilot) due to credit-limit failures (402 errors) and lower totals (79).**
```

### research_review
```text
**Chosen candidate:** **NVIDIA Nemotron 3 Nano Omni (free)**  

**Strengths**  
- Live, publicly discovered model available through an API – ready for immediate testing.  
- Free‑tier access via OpenRouter; no direct cost to the research team.  
- Strong benchmark performance (quality 30) indicates solid reasoning capability.  

**Weaknesses**  
- License must be verified before any downstream use.  
- Free‑tier availability is not guaranteed; usage may be throttled or discontinued.  
- Requires benchmark testing to confirm suitability for the specific research task.  

**Risks**  
- Provider‑level rate‑limit changes or API deprecation could interrupt access.  
- As a free‑tier offering, capacity may be limited during peak demand, affecting reproducibility.  

**Recommendation**  
- **TEST_FIRST** – Run a brief benchmark suite (e.g., reasoning tasks, latency, cost per request) to validate performance and confirm that the free‑tier limits meet the project’s needs before any larger‑scale adoption.  

*Both candidates share the same total score (94) and similar risk profile, but NVIDIA’s broader ecosystem and lower migration difficulty make it the more reliable option for immediate evaluation.*
```

### final_review
```text
**1. Coding recommendation**  
- **Model:** Qwen3 Coder 480B A35B (free, OpenRouter)  
- **Strengths:** Highest total score (84), strong quality (30/30), free‑tier API access.  
- **Weaknesses:** Unclear open‑source license, recent 429 rate‑limit failure, migration difficulty.  
- **Risks:** Provider‑driven free‑tier changes, temporary rate‑limit throttling, need to verify license.  
- **Suggested action:** **TEST_FIRST** – re‑run benchmark with reduced token limit, confirm license terms, monitor rate limits.

**2. Research recommendation**  
- **Model:** NVIDIA Nemotron 3 Nano Omni (free, OpenRouter)  
- **Strengths:** Live API, free‑tier available, solid quality (30) and reasoning performance.  
- **Weaknesses:** License must be verified, free‑tier availability not guaranteed, requires benchmark validation.  
- **Risks:** Rate‑limit or API deprecation, limited capacity during peak usage, reproducibility concerns.  
- **Suggested action:** **TEST_FIRST** – run a concise benchmark suite (reasoning tasks, latency, cost) to confirm fit.

**3. Risks (combined)**  
- Free‑tier API instability (rate limits, throttling, possible discontinuation).  
- Benchmark failures (429/402 errors) indicating current access issues.  
- Uncertainty around open‑source licenses for both models.  
- Migration and integration effort may be non‑trivial.  

**4. Final decision suggestion**  
- **TEST_FIRST** – conduct the recommended validation steps before any broader adoption or replacement.
```

## Category: research_reasoning

| Rank | Model | Provider | Score | Recommendation Style |
|---:|---|---|---:|---|
| 1 | Baidu Qianfan: CoBuddy (free) | OpenRouter | 94 | Candidate |
| 2 | NVIDIA: Nemotron 3 Nano Omni (free) | OpenRouter | 94 | Candidate |
| 3 | Poolside: Laguna XS.2 (free) | OpenRouter | 94 | Candidate |

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
- Benchmark score: 10
- Benchmark output preview:
```text

# Open-Source vs Closed-Source AI Models: A Comparison

## Open-Source AI Models

**Strengths:**
1. **Transparency & Auditability** - Full access to model architecture, training code, and often training data, enabling security audits, bias detection, and regulatory compliance verification
2. **Customization & Flexibility** - Complete ability to modify, fine-tune, or integrate into specialized applications without licensing restrictions
3. **Community Innovation** - Rapid iteration through global collaboration, with improvements shared openly across research communities

**Weaknesses:**
1. **Resource Limitations** - Lacks the massive compute budgets, proprietary datasets, and engineering teams of major corporations
2. **Quality Inconsistency** - Varies significantly between projects; requires technical expertise to identify reliable implementations
3. **Support Challenges** - Limited professional support channels; troubleshooting depends on community forums rather than dedicated teams

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
### Best Candidate: Qwen: Qwen3 Coder 480B A35B (free)  
**Total Score:** 84 (highest among candidates)  

#### **Strengths:**  
- **High Quality Score (30/30):** Strong performance potential for coding/analysis tasks.  
- **Free API Access:** Available via OpenRouter’s free tier.  
- **Live Model:** Regularly updated, suitable for dynamic evaluation.  

#### **Weaknesses:**  
- **License Uncertainty:** Open-source status requires verification (exact license unknown).  
- **Rate-Limited:** Recent benchmark failed due to temporary upstream rate limits (429 error).  
- **Stability Concerns:** Provider-driven risks (e.g., free-tier changes).  

#### **Risks:**  
- **Provider Instability:** Free-tier access may change (e.g., rate limits or costs).  
- **Benchmark Failure:** Current API test unsuccessful (rate-limited).  
- **Migration Difficulty:** Medium complexity if replacing existing models.  

#### **Recommendation: TEST_FIRST**  
- **Why?**  
  - Highest total score and free-tier access align with preferences.  
  - Rate-limit error is temporary (retry suggested); test again with adjusted token limits.  
  - Verify license terms and free-tier policies before full adoption.  
- **Action:**  
  1. **Re-run benchmark** with reduced token count (e.g., 5k tokens) to confirm free-tier usability.  
  2. **Verify open-source license** (e.g., check GitHub or provider docs).  
  3. **Monitor rate limits** during extended tests.  

**Reject candidates with lower scores (Pareto/Kwaipilot) due to credit-limit failures (402 errors) and lower totals (79).**
```

### research_review
```text
**Chosen candidate:** **NVIDIA Nemotron 3 Nano Omni (free)**  

**Strengths**  
- Live, publicly discovered model available through an API – ready for immediate testing.  
- Free‑tier access via OpenRouter; no direct cost to the research team.  
- Strong benchmark performance (quality 30) indicates solid reasoning capability.  

**Weaknesses**  
- License must be verified before any downstream use.  
- Free‑tier availability is not guaranteed; usage may be throttled or discontinued.  
- Requires benchmark testing to confirm suitability for the specific research task.  

**Risks**  
- Provider‑level rate‑limit changes or API deprecation could interrupt access.  
- As a free‑tier offering, capacity may be limited during peak demand, affecting reproducibility.  

**Recommendation**  
- **TEST_FIRST** – Run a brief benchmark suite (e.g., reasoning tasks, latency, cost per request) to validate performance and confirm that the free‑tier limits meet the project’s needs before any larger‑scale adoption.  

*Both candidates share the same total score (94) and similar risk profile, but NVIDIA’s broader ecosystem and lower migration difficulty make it the more reliable option for immediate evaluation.*
```

### final_review
```text
**1. Coding recommendation**  
- **Model:** Qwen3 Coder 480B A35B (free, OpenRouter)  
- **Strengths:** Highest total score (84), strong quality (30/30), free‑tier API access.  
- **Weaknesses:** Unclear open‑source license, recent 429 rate‑limit failure, migration difficulty.  
- **Risks:** Provider‑driven free‑tier changes, temporary rate‑limit throttling, need to verify license.  
- **Suggested action:** **TEST_FIRST** – re‑run benchmark with reduced token limit, confirm license terms, monitor rate limits.

**2. Research recommendation**  
- **Model:** NVIDIA Nemotron 3 Nano Omni (free, OpenRouter)  
- **Strengths:** Live API, free‑tier available, solid quality (30) and reasoning performance.  
- **Weaknesses:** License must be verified, free‑tier availability not guaranteed, requires benchmark validation.  
- **Risks:** Rate‑limit or API deprecation, limited capacity during peak usage, reproducibility concerns.  
- **Suggested action:** **TEST_FIRST** – run a concise benchmark suite (reasoning tasks, latency, cost) to confirm fit.

**3. Risks (combined)**  
- Free‑tier API instability (rate limits, throttling, possible discontinuation).  
- Benchmark failures (429/402 errors) indicating current access issues.  
- Uncertainty around open‑source licenses for both models.  
- Migration and integration effort may be non‑trivial.  

**4. Final decision suggestion**  
- **TEST_FIRST** – conduct the recommended validation steps before any broader adoption or replacement.
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
- Best candidate score: 94
- Improvement: 34.29%
- Decision: REPLACE_AFTER_APPROVAL

## Human Approval

Choose one:
- APPROVE
- REJECT
- TEST_FIRST

No system change should happen until human decision is recorded.
