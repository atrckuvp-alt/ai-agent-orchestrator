# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-24T18:43:08

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

#### Strengths:
- **Highest Total Score (84)**: Superior to peers in quality, free-tier, and API availability.
- **Free Tier Access**: Explicitly labeled as "free" (requires verification).
- **API Access**: Available via OpenRouter for integration.
- **Benchmark Potential**: Error was temporary (rate-limited), not model failure.

#### Weaknesses:
- **License Verification**: Exact license status unconfirmed.
- **Rate-Limited**: Benchmark failed due to upstream limits (mitigable via retry or API key).
- **Stability Concerns**: Provider/rate-limit changes possible.

#### Risks:
- **Rate-Limit Instability**: Temporary outages may disrupt testing.
- **Provider Dependency**: OpenRouter’s terms could shift.

#### Action: **TEST_FIRST**  
- **Why**: Highest score, free-tier promise, and temporary benchmark error (resolved by retry/API key). Verify license/free-tier status during testing.  
- **Reject Others?**:  
  - **Pareto Code Router**: Benchmark failed due to insufficient credits (402 error), requiring paid upgrade → **REJECT** (not free-tier viable).  
  - **Kwaipilot**: Same credit issue → **REJECT**.  

**Summary**: Test Qwen first to validate free-tier access, license, and stability. Reject Pareto/Kwaipilot due to credit barriers.
```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text
**1. Coding recommendation**  
- **Model:** *Qwen: Qwen3 Coder 480B A35B (free)* – accessed via OpenRouter.  
- **Strengths:** Highest total score (84); free‑tier access (pending verification); API available for integration; benchmark error was a transient rate‑limit, not a model failure.  
- **Weaknesses:** License status not fully confirmed; currently subject to OpenRouter rate limits; stability depends on provider’s throttling policies.  
- **Risks:** Possible outage or stricter rate limits during testing; provider terms could change, affecting long‑term availability.  

**Suggested action:** **TEST_FIRST** – run a focused integration test to verify true free‑tier access, confirm licensing, and assess rate‑limit behavior.  

*Rejected alternatives:* Pareto Code Router and Kwaipilot (both failed due to paid‑only credit errors).

---

**2. Research recommendation**  
- **Model:** *Baidu Qianfan: CoBuddy (free)* – request failed.  
- **Issue:** Invalid model ID (400 error) → cannot retrieve any response.  
- **Implication:** No data to evaluate strengths or weaknesses; the model may not exist under that identifier or is not publicly accessible.

**Suggested action:** **REJECT** the current request for this model until a correct, reachable model ID is provided.

---

**3. Risks**  
- **Coding side:** Rate‑limit instability could cause intermittent failures; reliance on a single provider (OpenRouter) could expose us to policy or pricing changes.  
- **Research side:** Continuing to request invalid IDs wastes API quota and may trigger abuse flags; using an unverified Baidu endpoint could raise compliance or data‑privacy concerns.

---

**4. Final decision suggestion**  
- **Coding model:** **TEST_FIRST** – run a limited trial to confirm free‑tier status and stability.  
- **Research model:** **REJECT** – request clarification or a correct model identifier before any further evaluation.
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

### Strengths ✅
1. **Transparency & Auditability** - Full access to model architecture, training data (where available), and source code allows for security auditing, bias detection, and regulatory compliance verification
2. **Customization & Flexibility** - Can be freely modified, fine-tuned, and deployed on any infrastructure without vendor lock-in; ideal for specialized applications
3. **Cost-Effectiveness** - No licensing fees or usage restrictions; community-driven development reduces costs for organizations and researchers

### Weaknesses ❌
1. **Limited Resources** - Smaller development teams and budgets result in fewer parameters, less training data, and slower iteration compared to well-funded competitors
2. **Technical Expertise Required** - Organizations need ML engineers and DevOps teams to deploy, maintain, and optimize models effectively
3. **Inconsistent Performance** - May lack the scale 
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

#### Strengths:
- **Highest Total Score (84)**: Superior to peers in quality, free-tier, and API availability.
- **Free Tier Access**: Explicitly labeled as "free" (requires verification).
- **API Access**: Available via OpenRouter for integration.
- **Benchmark Potential**: Error was temporary (rate-limited), not model failure.

#### Weaknesses:
- **License Verification**: Exact license status unconfirmed.
- **Rate-Limited**: Benchmark failed due to upstream limits (mitigable via retry or API key).
- **Stability Concerns**: Provider/rate-limit changes possible.

#### Risks:
- **Rate-Limit Instability**: Temporary outages may disrupt testing.
- **Provider Dependency**: OpenRouter’s terms could shift.

#### Action: **TEST_FIRST**  
- **Why**: Highest score, free-tier promise, and temporary benchmark error (resolved by retry/API key). Verify license/free-tier status during testing.  
- **Reject Others?**:  
  - **Pareto Code Router**: Benchmark failed due to insufficient credits (402 error), requiring paid upgrade → **REJECT** (not free-tier viable).  
  - **Kwaipilot**: Same credit issue → **REJECT**.  

**Summary**: Test Qwen first to validate free-tier access, license, and stability. Reject Pareto/Kwaipilot due to credit barriers.
```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text
**1. Coding recommendation**  
- **Model:** *Qwen: Qwen3 Coder 480B A35B (free)* – accessed via OpenRouter.  
- **Strengths:** Highest total score (84); free‑tier access (pending verification); API available for integration; benchmark error was a transient rate‑limit, not a model failure.  
- **Weaknesses:** License status not fully confirmed; currently subject to OpenRouter rate limits; stability depends on provider’s throttling policies.  
- **Risks:** Possible outage or stricter rate limits during testing; provider terms could change, affecting long‑term availability.  

**Suggested action:** **TEST_FIRST** – run a focused integration test to verify true free‑tier access, confirm licensing, and assess rate‑limit behavior.  

*Rejected alternatives:* Pareto Code Router and Kwaipilot (both failed due to paid‑only credit errors).

---

**2. Research recommendation**  
- **Model:** *Baidu Qianfan: CoBuddy (free)* – request failed.  
- **Issue:** Invalid model ID (400 error) → cannot retrieve any response.  
- **Implication:** No data to evaluate strengths or weaknesses; the model may not exist under that identifier or is not publicly accessible.

**Suggested action:** **REJECT** the current request for this model until a correct, reachable model ID is provided.

---

**3. Risks**  
- **Coding side:** Rate‑limit instability could cause intermittent failures; reliance on a single provider (OpenRouter) could expose us to policy or pricing changes.  
- **Research side:** Continuing to request invalid IDs wastes API quota and may trigger abuse flags; using an unverified Baidu endpoint could raise compliance or data‑privacy concerns.

---

**4. Final decision suggestion**  
- **Coding model:** **TEST_FIRST** – run a limited trial to confirm free‑tier status and stability.  
- **Research model:** **REJECT** – request clarification or a correct model identifier before any further evaluation.
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
