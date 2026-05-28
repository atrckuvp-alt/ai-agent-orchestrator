# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-22T20:13:31

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
### Best Candidate: **Qwen: Qwen3 Coder 480B A35B (free)**  

#### **Strengths**  
- **Highest score** (84/100) among candidates, indicating overall strong potential.  
- **Free-tier availability** (score: 15/15) suggests generous free access.  
- **API-compatible** (score: 15/15) and designed for dynamic evaluation.  

#### **Weaknesses**  
- **License unverified** (must confirm open-source status).  
- **Benchmark failed** (rate-limited error; requires retry or API key).  
- **Availability risk** (provider may change free-tier terms).  

#### **Risks**  
- **Rate-limiting** (429 error during testing; may disrupt workflows).  
- **Dependency** on OpenRouter’s terms (e.g., credit requirements for heavy usage).  

#### **Recommendation: TEST_FIRST**  
- **Why?**  
  - Highest score and free-tier access make it most promising.  
  - Rate-limiting is temporary and resolvable via API key or retry.  
  - Other candidates failed due to insufficient credits (fundamental free-tier flaw), while Qwen’s issue is operational.  
- **Human Action Required**:  
  1. Verify license and free-tier terms.  
  2. Test with reduced token counts or an API key.  
  3. If unstable, reject; otherwise, proceed.  

**Note**: Pareto Code Router and Kwaipilot were rejected due to lower scores (79/100) and credit-based failures, indicating weaker free-tier viability.
```

### research_review
```text
**Best Candidate:** *Baidu Qianfan: CoBuddy (free)*

**Strengths:**  
- Live discovered model with real user interactions.  
- API-friendly, suitable for dynamic evaluation and testing.  
- Aligns with open-source transparency and collaborative research goals.

**Weaknesses:**  
- License details require verification.  
- Availability can change based on provider decisions.  
- Needs thorough benchmarking before deployment.

**Risks:**  
- License compliance risks if not vetted.  
- Potential rate limits or access changes from provider.  
- Necesitates human validation before full integration.

**Recommendation:**  
Human should **TEST_FIRST** due to licensing ambiguities, resource constraints, and the need for rigorous evaluation before committing to integration or deployment. Validate open-source documentation and perform small-scale benchmarking.
```

### final_review
```text
**1.Coding recommendation**  
- **Candidate:** Qwen : Qwen3 Coder 480B A35B (free) via OpenRouter.  
- **Why:** Highest benchmark score (84/100) and full free‑tier rating (15/15); API‑compatible and designed for dynamic evaluation.  - **Caveats:** License not yet verified; benchmark failed due to OpenRouter rate‑limit (429).  

**2. Research recommendation**  
- **Candidate:** Baidu Qianfan : CoBuddy (free).  
- **Why:** Currently live, API‑friendly, and aligns with open‑source transparency goals.  - **Caveats:** License details pending verification; availability may shift; requires thorough benchmarking.  

**3. Risks**  - **Rate‑limiting / credit constraints** – OpenRouter may throttle or require credits for sustained usage.  
- **License ambiguity** – Must confirm open‑source status for both Qwen and CoBuddy; non‑compliance could block deployment.  
- **Stability of free‑tier** – Provider‑level policy changes could remove or restrict free access.  - **Benchmark reliability** – Initial failures (rate‑limit, credit exhaustion) indicate operational fragility.  

**4. Final decision suggestion:** **TEST_FIRST**  
- **Human Action Required (by [Researcher]):**  
  1. Verify the open‑source license for Qwen Coder 480B A35B and for CoBuddy.  
  2. Re‑run the benchmark with an API key or reduced token counts to mitigate rate‑limit issues.  
  3. Perform a small‑scale benchmark on CoBuddy to assess performance and stability.  
  4. If verification succeeds and stability improves, proceed to integration; otherwise, reject or switch to an alternative.
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

I'd be happy to break down the comparison between open-source and closed-source AI models for you!

## Open-Source AI Models

**Strengths:**
1. **Transparency & Control** - You can inspect the code, modify architectures, and understand exactly how the model works. This builds trust and allows for deep customization.
2. **Cost-Effective** - Typically free to use and deploy, with no per-token fees or subscription costs for the underlying model.
3. **Community Innovation** - Rapid iteration from global developer communities leads to quick improvements and specialized variants.

**Weaknesses:**
1. **Resource Limitations** - Often lack the massive computational budgets and diverse training data that big tech companies have.
2. **Support Challenges** - Community-driven help rather than professional support teams, documentation can be inconsistent.
3. **Performance Gap** - May trail behind cutting-edge closed models in complex reasoning and instruction-following abilities.

## Closed-Source 
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
### Best Candidate: **Qwen: Qwen3 Coder 480B A35B (free)**  

#### **Strengths**  
- **Highest score** (84/100) among candidates, indicating overall strong potential.  
- **Free-tier availability** (score: 15/15) suggests generous free access.  
- **API-compatible** (score: 15/15) and designed for dynamic evaluation.  

#### **Weaknesses**  
- **License unverified** (must confirm open-source status).  
- **Benchmark failed** (rate-limited error; requires retry or API key).  
- **Availability risk** (provider may change free-tier terms).  

#### **Risks**  
- **Rate-limiting** (429 error during testing; may disrupt workflows).  
- **Dependency** on OpenRouter’s terms (e.g., credit requirements for heavy usage).  

#### **Recommendation: TEST_FIRST**  
- **Why?**  
  - Highest score and free-tier access make it most promising.  
  - Rate-limiting is temporary and resolvable via API key or retry.  
  - Other candidates failed due to insufficient credits (fundamental free-tier flaw), while Qwen’s issue is operational.  
- **Human Action Required**:  
  1. Verify license and free-tier terms.  
  2. Test with reduced token counts or an API key.  
  3. If unstable, reject; otherwise, proceed.  

**Note**: Pareto Code Router and Kwaipilot were rejected due to lower scores (79/100) and credit-based failures, indicating weaker free-tier viability.
```

### research_review
```text
**Best Candidate:** *Baidu Qianfan: CoBuddy (free)*

**Strengths:**  
- Live discovered model with real user interactions.  
- API-friendly, suitable for dynamic evaluation and testing.  
- Aligns with open-source transparency and collaborative research goals.

**Weaknesses:**  
- License details require verification.  
- Availability can change based on provider decisions.  
- Needs thorough benchmarking before deployment.

**Risks:**  
- License compliance risks if not vetted.  
- Potential rate limits or access changes from provider.  
- Necesitates human validation before full integration.

**Recommendation:**  
Human should **TEST_FIRST** due to licensing ambiguities, resource constraints, and the need for rigorous evaluation before committing to integration or deployment. Validate open-source documentation and perform small-scale benchmarking.
```

### final_review
```text
**1.Coding recommendation**  
- **Candidate:** Qwen : Qwen3 Coder 480B A35B (free) via OpenRouter.  
- **Why:** Highest benchmark score (84/100) and full free‑tier rating (15/15); API‑compatible and designed for dynamic evaluation.  - **Caveats:** License not yet verified; benchmark failed due to OpenRouter rate‑limit (429).  

**2. Research recommendation**  
- **Candidate:** Baidu Qianfan : CoBuddy (free).  
- **Why:** Currently live, API‑friendly, and aligns with open‑source transparency goals.  - **Caveats:** License details pending verification; availability may shift; requires thorough benchmarking.  

**3. Risks**  - **Rate‑limiting / credit constraints** – OpenRouter may throttle or require credits for sustained usage.  
- **License ambiguity** – Must confirm open‑source status for both Qwen and CoBuddy; non‑compliance could block deployment.  
- **Stability of free‑tier** – Provider‑level policy changes could remove or restrict free access.  - **Benchmark reliability** – Initial failures (rate‑limit, credit exhaustion) indicate operational fragility.  

**4. Final decision suggestion:** **TEST_FIRST**  
- **Human Action Required (by [Researcher]):**  
  1. Verify the open‑source license for Qwen Coder 480B A35B and for CoBuddy.  
  2. Re‑run the benchmark with an API key or reduced token counts to mitigate rate‑limit issues.  
  3. Perform a small‑scale benchmark on CoBuddy to assess performance and stability.  
  4. If verification succeeds and stability improves, proceed to integration; otherwise, reject or switch to an alternative.
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
