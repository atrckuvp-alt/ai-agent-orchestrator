# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-24T00:34:01

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
**Chosen candidate:** **Qwen 3 Coder 480B A35B (free)** – `qwen/qwen3-coder:free` (OpenRouter)

---

### Strengths
| Aspect | Why it matters |
|--------|----------------|
| **Model size / capability** | 480 B parameters; state‑of‑the‑art for code generation and analysis. |
| **Open‑source claim** | Listed as “open‑source”; if the license is permissive it can be self‑hosted later. |
| **Free‑tier access** | Currently advertised as a free model on OpenRouter – no upfront cost for evaluation. |
| **API availability** | Immediate access via a standard OpenRouter endpoint, simplifying integration. |
| **Dynamic evaluation** | Large enough to handle complex coding tasks, unit‑test generation, and reasoning. |

### Weaknesses
| Issue | Impact |
|-------|--------|
| **License not yet verified** | May turn out to be non‑commercial or have usage restrictions; we must confirm before production use. |
| **Rate‑limiting** (HTTP 429) | The recent benchmark hit a temporary upstream limit; could affect reliability under load. |
| **Stability of free‑tier** | Free offering could be withdrawn or throttled without notice, affecting long‑term availability. |
| **Benchmark data missing** | No success metric yet; we lack concrete evidence of coding‑analysis quality versus alternatives. |

### Risks
1. **Compliance risk** – Using the model without a clear license could breach copyright or redistribution rules.  
2. **Operational risk** – Sudden rate‑limit or quota changes could break CI/CD pipelines that depend on the model.  
3. **Vendor lock‑in risk** – If the free tier is removed, we would need to migrate to another model (medium difficulty).  

### Recommendation
- **Human action:** **TEST_FIRST**  
  - Verify the exact license (e.g., Apache‑2.0, MIT, or a more restrictive one).  
  - Run a focused benchmark suite (unit‑test generation, bug‑fix suggestion, code review) to obtain a concrete quality score.  
  **If** the license is permissive and the benchmark meets our internal threshold, we can promote the model to production; otherwise **REJECT** and look for alternative open‑source, free‑tier options.

---
```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text
1. **Coding Recommendation:** TEST_FIRST  
2. **Research Recommendation:** Evaluation via OpenRouter model constraints  
3. **Risks:** License ambiguity, rate-limiting, potential instability of free-tier model  
4. **Final Decision Suggestion:** TEST_FIRST  

**Notes:**  
- Adheres to open-source priorities while emphasizing evidence gaps.  
- Risks mitigated by initial verification before full adoption.  
- Testing ensures compliance and reliability prior to deployment.
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

### **Strengths:**

1. **Transparency & Auditability** 🔍  
   Source code and model weights are publicly available, allowing developers to inspect, verify, and understand exactly how the system works. This builds trust and enables security auditing.

2. **Customization & Flexibility** ⚙️  
   Users can modify, fine-tune, or rebuild models for specific use cases without restrictions. Ideal for researchers, startups, and organizations with unique requirements.

3. **Community Innovation** 🤝  
   Collective development drives rapid iteration and diverse improvements. Multiple contributors bring different perspectives, accelerating advancement across various domains.

### **Weaknesses:**

1. **Resource Limitations** 💰  
   Often developed by smaller teams or individuals with limited funding, resulting in fewer computational resources, smaller datasets, and less extensive testing compared to corporate-backed 
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
**Chosen candidate:** **Qwen 3 Coder 480B A35B (free)** – `qwen/qwen3-coder:free` (OpenRouter)

---

### Strengths
| Aspect | Why it matters |
|--------|----------------|
| **Model size / capability** | 480 B parameters; state‑of‑the‑art for code generation and analysis. |
| **Open‑source claim** | Listed as “open‑source”; if the license is permissive it can be self‑hosted later. |
| **Free‑tier access** | Currently advertised as a free model on OpenRouter – no upfront cost for evaluation. |
| **API availability** | Immediate access via a standard OpenRouter endpoint, simplifying integration. |
| **Dynamic evaluation** | Large enough to handle complex coding tasks, unit‑test generation, and reasoning. |

### Weaknesses
| Issue | Impact |
|-------|--------|
| **License not yet verified** | May turn out to be non‑commercial or have usage restrictions; we must confirm before production use. |
| **Rate‑limiting** (HTTP 429) | The recent benchmark hit a temporary upstream limit; could affect reliability under load. |
| **Stability of free‑tier** | Free offering could be withdrawn or throttled without notice, affecting long‑term availability. |
| **Benchmark data missing** | No success metric yet; we lack concrete evidence of coding‑analysis quality versus alternatives. |

### Risks
1. **Compliance risk** – Using the model without a clear license could breach copyright or redistribution rules.  
2. **Operational risk** – Sudden rate‑limit or quota changes could break CI/CD pipelines that depend on the model.  
3. **Vendor lock‑in risk** – If the free tier is removed, we would need to migrate to another model (medium difficulty).  

### Recommendation
- **Human action:** **TEST_FIRST**  
  - Verify the exact license (e.g., Apache‑2.0, MIT, or a more restrictive one).  
  - Run a focused benchmark suite (unit‑test generation, bug‑fix suggestion, code review) to obtain a concrete quality score.  
  **If** the license is permissive and the benchmark meets our internal threshold, we can promote the model to production; otherwise **REJECT** and look for alternative open‑source, free‑tier options.

---
```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text
1. **Coding Recommendation:** TEST_FIRST  
2. **Research Recommendation:** Evaluation via OpenRouter model constraints  
3. **Risks:** License ambiguity, rate-limiting, potential instability of free-tier model  
4. **Final Decision Suggestion:** TEST_FIRST  

**Notes:**  
- Adheres to open-source priorities while emphasizing evidence gaps.  
- Risks mitigated by initial verification before full adoption.  
- Testing ensures compliance and reliability prior to deployment.
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
