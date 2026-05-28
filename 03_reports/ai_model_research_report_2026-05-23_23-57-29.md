# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-23T23:57:29

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
## Analysis & Recommendation

### Candidate Comparison

| Model | Total Score | Free Tier Score | Benchmark Error | Error Type |
|-------|-------------|-----------------|-----------------|------------|
| **Qwen3 Coder 480B** | 84 | 15 | Rate-limited (429) | Transient |
| Pareto Code Router | 79 | 10 | Payment required (402) | Blocking |
| KAT-Coder-Pro V2 | 79 | 10 | Payment required (402) | Blocking |

---

### Best Candidate: **Qwen: Qwen3 Coder 480B A35B (free)**

#### Strengths
- **Highest total score** (84 vs 79)
- **Highest free_tier score** (15 vs 10) - indicates better free access
- **Transient error** - rate-limiting (429) is temporary; model is reachable
- Available via OpenRouter API

#### Weaknesses
- License must be verified (open_source_status: "verify exact license")
- Free-tier status must be verified
- Needs benchmark testing to confirm capability

#### Risks
- Provider/rate-limit changes (documented in benchmark)
- Availability may change without notice
- Migration difficulty: medium

---

### Recommendation

**TEST_FIRST**

**Rationale:**
1. Qwen is the only candidate with a *transient* error (rate-limiting), not a blocking error (payment required)
2. Highest scores across quality, free_tier, and total
3. Rate-limiting suggests the model is live and functional - just temporarily busy
4. The other two candidates require payment to test, making them unsuitable for free-tier evaluation

**Action:** Retry Qwen after brief delay to confirm rate-limit has lifted. If successful, proceed with benchmark testing. Verify license and free-tier terms before production use.
```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text

## Combined Review Summary

### 1. Coding Recommendation
**TEST_FIRST** - Qwen3 Coder 480B A35B (free)
- **Score**: 84 total / 15 free tier (highest among candidates)
- **Error**: Rate-limited (429) - transient, not blocking
- **Strengths**: Highest quality score, better free-tier access, model is live and functional
- **Weaknesses**: License verification needed, free-tier terms must be confirmed

### 2. Research Recommendation
**INCOMPLETE** - Research agent failed
- **Error**: Invalid model ID "Baidu Qianfan: CoBuddy (free)" (HTTP 400)
- **Impact**: No research validation could be performed
- **Action Required**: Resolve model ID or select alternative research model

### 3. Risks
- **Provider volatility**: Rate-limit changes documented; availability may shift without notice
- **License uncertainty**: Qwen license status requires verification before production
- **Incomplete evaluation**: Research review missing due to invalid model ID
- **Migration overhead**: Medium difficulty if provider terms change
- **Temporal limitation**: Free-tier status may not persist

### 4. Final Decision Suggestion: **TEST_FIRST**

**Rationale**: 
- Qwen is the only viable free-tier candidate with transient (not blocking) errors
- Coding review shows measurable quality advantage and functional model availability
- Research review incomplete but doesn't block preliminary testing
- Low-risk approach aligns with preference for free-tier models

**Next Steps**: 
1. Retry Qwen after brief delay to confirm rate-limit clearance
2. Resolve research agent model ID issue for additional validation
3. Verify license and free-tier terms before any production consideration

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

Here's a comparison of **open-source AI models** and **closed-source AI models**, with their key strengths and weaknesses:

---

### **Open-Source AI Models**  
**Strengths:**  
1. **Customization & Flexibility**: Users can modify the model architecture, training data, or weights to suit specific needs.  
2. **Transparency**: Code, training data, and sometimes even weights are publicly available, allowing scrutiny and trust-building.  
3. **Cost-Effective**: No licensing fees; often free to use, train, or deploy, making them accessible to smaller organizations or hobbyists.  

**Weaknesses:**  
1. **Limited Resources**: Often lack the computational power, data, or expertise of large corporations, leading to lower performance in some tasks.  
2. **Community-Driven Support**: Relies on volunteer communities for updates, bug fixes, and documentation, which may be inconsistent.  
3. **Security Risks**: Publicly accessible code/weights could expose vulnerabilities or be misused without pro
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
## Analysis & Recommendation

### Candidate Comparison

| Model | Total Score | Free Tier Score | Benchmark Error | Error Type |
|-------|-------------|-----------------|-----------------|------------|
| **Qwen3 Coder 480B** | 84 | 15 | Rate-limited (429) | Transient |
| Pareto Code Router | 79 | 10 | Payment required (402) | Blocking |
| KAT-Coder-Pro V2 | 79 | 10 | Payment required (402) | Blocking |

---

### Best Candidate: **Qwen: Qwen3 Coder 480B A35B (free)**

#### Strengths
- **Highest total score** (84 vs 79)
- **Highest free_tier score** (15 vs 10) - indicates better free access
- **Transient error** - rate-limiting (429) is temporary; model is reachable
- Available via OpenRouter API

#### Weaknesses
- License must be verified (open_source_status: "verify exact license")
- Free-tier status must be verified
- Needs benchmark testing to confirm capability

#### Risks
- Provider/rate-limit changes (documented in benchmark)
- Availability may change without notice
- Migration difficulty: medium

---

### Recommendation

**TEST_FIRST**

**Rationale:**
1. Qwen is the only candidate with a *transient* error (rate-limiting), not a blocking error (payment required)
2. Highest scores across quality, free_tier, and total
3. Rate-limiting suggests the model is live and functional - just temporarily busy
4. The other two candidates require payment to test, making them unsuitable for free-tier evaluation

**Action:** Retry Qwen after brief delay to confirm rate-limit has lifted. If successful, proceed with benchmark testing. Verify license and free-tier terms before production use.
```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text

## Combined Review Summary

### 1. Coding Recommendation
**TEST_FIRST** - Qwen3 Coder 480B A35B (free)
- **Score**: 84 total / 15 free tier (highest among candidates)
- **Error**: Rate-limited (429) - transient, not blocking
- **Strengths**: Highest quality score, better free-tier access, model is live and functional
- **Weaknesses**: License verification needed, free-tier terms must be confirmed

### 2. Research Recommendation
**INCOMPLETE** - Research agent failed
- **Error**: Invalid model ID "Baidu Qianfan: CoBuddy (free)" (HTTP 400)
- **Impact**: No research validation could be performed
- **Action Required**: Resolve model ID or select alternative research model

### 3. Risks
- **Provider volatility**: Rate-limit changes documented; availability may shift without notice
- **License uncertainty**: Qwen license status requires verification before production
- **Incomplete evaluation**: Research review missing due to invalid model ID
- **Migration overhead**: Medium difficulty if provider terms change
- **Temporal limitation**: Free-tier status may not persist

### 4. Final Decision Suggestion: **TEST_FIRST**

**Rationale**: 
- Qwen is the only viable free-tier candidate with transient (not blocking) errors
- Coding review shows measurable quality advantage and functional model availability
- Research review incomplete but doesn't block preliminary testing
- Low-risk approach aligns with preference for free-tier models

**Next Steps**: 
1. Retry Qwen after brief delay to confirm rate-limit clearance
2. Resolve research agent model ID issue for additional validation
3. Verify license and free-tier terms before any production consideration

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
