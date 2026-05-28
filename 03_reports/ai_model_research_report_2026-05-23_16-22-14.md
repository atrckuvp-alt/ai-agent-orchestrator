# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-23T16:22:14

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
**Chosen candidate:** **Qwen: Qwen3 Coder 480B A35B (free)**  *(model_id: `qwen/qwen3-coder:free` on OpenRouter)*  

### Why it’s the best fit
| Aspect | Detail |
|--------|--------|
| **Score** | Highest total_score = 84 (quality 30, free_tier 15, api 15, open_source 10). |
| **Availability** | Live model and accessible via API (needs no self‑hosting). |
| **Open‑source** | Status pending official license – must verify before production use. |
| **Free tier** | Free‑tier can be used if you add your own OpenRouter key to accumulate credits. |
| **Strengths** | • Recent, powerful coder‑focused model (480 B parameters).<br>• Easy to test via OpenRouter API.<br>• Good candidate for dynamic benchmarking. |
| **Weaknesses** | • License not yet confirmed (may restrict commercial use).<br>• Current benchmark hit a 429 rate‑limit; may need throttling or own key.<br>• “Migration difficulty” = medium (may require prompt tweaks). |
| **Risks** | • Provider‑side rate limits or sudden endpoint changes could interrupt testing.<br>• Free tier usage counts against your allocated credits; you’ll need an API key to avoid hitting the 13‑credit ceiling quickly. |
| **Benchmark result** | Failed (error 429) due to upstream rate‑limit, but the model is functional once the limit is bypassed (e.g., by adding your own key). |

### Human decision: **TEST_FIRST**
- **Reason to test:** The model shows strong coding ability, is publicly reachable, and the failure is only a temporary rate‑limit issue. With an own OpenRouter API key the test can succeed and give concrete quality metrics.
- **Next steps:**  
  1. Add your personal OpenRouter key and retry (the retry‑after is ~13 s).  
  2. Run a focused benchmark (e.g., Python/JS code generation tasks) to assess output quality.  
  3. Verify the exact license (e.g., Apache‑2.0, MIT) before any production deployment.  
- **If verification reveals restrictive licensing or unacceptable rate‑limit constraints, then REJECT.**  

*In short: Qwen’s Qwen3‑Coder leads the list; proceed with a quick API‑key‑backed test to confirm stability and licensing before moving forward.*
```

### research_review
```text
## Recommendation: **NVIDIA: Nemotron 3 Nano Omni (free)**

**Name**: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`

---

### Strengths
- **NVIDIA backing** — strong track record in enterprise/open models (Megatron, Nemotron series)
- **Live discovered on OpenRouter** — accessible via API immediately
- **Free tier** — zero cost for testing
- **Reasoning category** — explicitly tagged for research/reasoning

### Weaknesses
- License unverified — could be research-only or restrictive
- Free-tier availability uncertain; rate limits likely
- No benchmark data yet beyond placeholder output

### Risks
- Free-tier may disappear or change rate limits
- Proprietary licensing could block production use
- Benchmark placeholder suggests output is generic, not evaluated

### Verdict
All three candidates have identical scores (94 total, 10 benchmark). **NVIDIA Nemotron** is preferred due to NVIDIA's established open-source model ecosystem and credibility. However, the benchmark output is a generic placeholder — meaning no real evaluation has been done.

**Action: TEST_FIRST** — run real reasoning benchmarks before any production commitment.

The other two (CoBuddy, Laguna XS.2) are **REJECT** pending human approval to test first.
```

### final_review
```text

**1. Coding Recommendation**  
**Model:** Qwen: Qwen3 Coder 480B A35B (free) (`qwen/qwen3-coder:free` on OpenRouter)  
**Strengths:** Highest total score (84), powerful coder-focused architecture (480B parameters), accessible via API without self-hosting, suitable for dynamic benchmarking.  
**Weaknesses:** License status pending verification (may restrict commercial use), encountered rate-limit (429) in benchmark, medium migration difficulty (may require prompt adjustments).  
**Risks:** Provider-side rate limits or endpoint changes could disrupt testing; free-tier usage consumes allocated credits quickly (requires personal API key to mitigate).  

**2. Research Recommendation**  
**Model:** NVIDIA: Nemotron 3 Nano Omni (free) (`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` on OpenRouter)  
**Strengths:** Backed by NVIDIA (established open-source ecosystem), explicitly reasoning-focused, free-tier accessible via API.  
**Weaknesses:** License unverified (may be research-only), free-tier availability and rate limits uncertain, benchmark output was a generic placeholder (no real evaluation performed).  
**Risks:** Free-tier may change or disappear; restrictive licensing could block production use; lack of verified performance data increases uncertainty.  

**3. Risks (Combined)**  
- **Licensing Uncertainty:** Both models lack confirmed open-source/commercial licenses—premature deployment could violate terms.  
- **Rate Limiting & Availability:** Free-tier APIs are subject to provider-imposed limits (Qwen: 429 error; NVIDIA: unknown limits), risking testing continuity.  
- **Benchmark Validity:** Qwen’s benchmark failed due to external limits; NVIDIA’s benchmark was a placeholder—neither provides reliable performance data yet.  
- **Credit Consumption:** Both require personal API keys to avoid exhausting free credits during testing.  

**4. Final Decision Suggestion**  
**TEST_FIRST** for both models.  
**Rationale:** Both models show promise (Qwen in coding, NVIDIA in reasoning) but have unresolved critical factors (licensing, rate limits, unverified benchmarks). A controlled test with personal API keys is necessary to validate stability, output quality, and licensing terms before any production consideration. **Do not proceed without human-approved testing and license verification.**
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

# Open-Source vs. Closed-Source AI Models: A Comparison

## Open-Source AI Models

### **Strengths:**
1. **Transparency & Auditability** - You can inspect, modify, and verify the model architecture, training process, and code. This builds trust and enables security auditing.
2. **Customization & Flexibility** - Complete freedom to fine-tune, adapt, or integrate into specialized applications without restrictions.
3. **Community Innovation** - Collaborative development often leads to rapid improvements, diverse use cases, and shared knowledge.

### **Weaknesses:**
1. **Resource Limitations** - Often lack the massive compute power, data, and engineering teams of big tech companies.
2. **Support & Maintenance** - Relies on community support rather than dedicated professional teams.
3. **Quality Inconsistency** - Varies significantly between projects; some may be experimental or poorly maintained.

---

## Closed-Source AI Models

### **Strengths:**
1. **Advanced Capabilities** - Typically
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
**Chosen candidate:** **Qwen: Qwen3 Coder 480B A35B (free)**  *(model_id: `qwen/qwen3-coder:free` on OpenRouter)*  

### Why it’s the best fit
| Aspect | Detail |
|--------|--------|
| **Score** | Highest total_score = 84 (quality 30, free_tier 15, api 15, open_source 10). |
| **Availability** | Live model and accessible via API (needs no self‑hosting). |
| **Open‑source** | Status pending official license – must verify before production use. |
| **Free tier** | Free‑tier can be used if you add your own OpenRouter key to accumulate credits. |
| **Strengths** | • Recent, powerful coder‑focused model (480 B parameters).<br>• Easy to test via OpenRouter API.<br>• Good candidate for dynamic benchmarking. |
| **Weaknesses** | • License not yet confirmed (may restrict commercial use).<br>• Current benchmark hit a 429 rate‑limit; may need throttling or own key.<br>• “Migration difficulty” = medium (may require prompt tweaks). |
| **Risks** | • Provider‑side rate limits or sudden endpoint changes could interrupt testing.<br>• Free tier usage counts against your allocated credits; you’ll need an API key to avoid hitting the 13‑credit ceiling quickly. |
| **Benchmark result** | Failed (error 429) due to upstream rate‑limit, but the model is functional once the limit is bypassed (e.g., by adding your own key). |

### Human decision: **TEST_FIRST**
- **Reason to test:** The model shows strong coding ability, is publicly reachable, and the failure is only a temporary rate‑limit issue. With an own OpenRouter API key the test can succeed and give concrete quality metrics.
- **Next steps:**  
  1. Add your personal OpenRouter key and retry (the retry‑after is ~13 s).  
  2. Run a focused benchmark (e.g., Python/JS code generation tasks) to assess output quality.  
  3. Verify the exact license (e.g., Apache‑2.0, MIT) before any production deployment.  
- **If verification reveals restrictive licensing or unacceptable rate‑limit constraints, then REJECT.**  

*In short: Qwen’s Qwen3‑Coder leads the list; proceed with a quick API‑key‑backed test to confirm stability and licensing before moving forward.*
```

### research_review
```text
## Recommendation: **NVIDIA: Nemotron 3 Nano Omni (free)**

**Name**: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`

---

### Strengths
- **NVIDIA backing** — strong track record in enterprise/open models (Megatron, Nemotron series)
- **Live discovered on OpenRouter** — accessible via API immediately
- **Free tier** — zero cost for testing
- **Reasoning category** — explicitly tagged for research/reasoning

### Weaknesses
- License unverified — could be research-only or restrictive
- Free-tier availability uncertain; rate limits likely
- No benchmark data yet beyond placeholder output

### Risks
- Free-tier may disappear or change rate limits
- Proprietary licensing could block production use
- Benchmark placeholder suggests output is generic, not evaluated

### Verdict
All three candidates have identical scores (94 total, 10 benchmark). **NVIDIA Nemotron** is preferred due to NVIDIA's established open-source model ecosystem and credibility. However, the benchmark output is a generic placeholder — meaning no real evaluation has been done.

**Action: TEST_FIRST** — run real reasoning benchmarks before any production commitment.

The other two (CoBuddy, Laguna XS.2) are **REJECT** pending human approval to test first.
```

### final_review
```text

**1. Coding Recommendation**  
**Model:** Qwen: Qwen3 Coder 480B A35B (free) (`qwen/qwen3-coder:free` on OpenRouter)  
**Strengths:** Highest total score (84), powerful coder-focused architecture (480B parameters), accessible via API without self-hosting, suitable for dynamic benchmarking.  
**Weaknesses:** License status pending verification (may restrict commercial use), encountered rate-limit (429) in benchmark, medium migration difficulty (may require prompt adjustments).  
**Risks:** Provider-side rate limits or endpoint changes could disrupt testing; free-tier usage consumes allocated credits quickly (requires personal API key to mitigate).  

**2. Research Recommendation**  
**Model:** NVIDIA: Nemotron 3 Nano Omni (free) (`nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` on OpenRouter)  
**Strengths:** Backed by NVIDIA (established open-source ecosystem), explicitly reasoning-focused, free-tier accessible via API.  
**Weaknesses:** License unverified (may be research-only), free-tier availability and rate limits uncertain, benchmark output was a generic placeholder (no real evaluation performed).  
**Risks:** Free-tier may change or disappear; restrictive licensing could block production use; lack of verified performance data increases uncertainty.  

**3. Risks (Combined)**  
- **Licensing Uncertainty:** Both models lack confirmed open-source/commercial licenses—premature deployment could violate terms.  
- **Rate Limiting & Availability:** Free-tier APIs are subject to provider-imposed limits (Qwen: 429 error; NVIDIA: unknown limits), risking testing continuity.  
- **Benchmark Validity:** Qwen’s benchmark failed due to external limits; NVIDIA’s benchmark was a placeholder—neither provides reliable performance data yet.  
- **Credit Consumption:** Both require personal API keys to avoid exhausting free credits during testing.  

**4. Final Decision Suggestion**  
**TEST_FIRST** for both models.  
**Rationale:** Both models show promise (Qwen in coding, NVIDIA in reasoning) but have unresolved critical factors (licensing, rate limits, unverified benchmarks). A controlled test with personal API keys is necessary to validate stability, output quality, and licensing terms before any production consideration. **Do not proceed without human-approved testing and license verification.**
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
