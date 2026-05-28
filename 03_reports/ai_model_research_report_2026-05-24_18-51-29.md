# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-24T18:51:29

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

Looking at these candidates, I need to analyze both the scores and the actual benchmark results to make a recommendation.

## Analysis Summary

| Candidate | Total Score | Benchmark Result | Actual Issue |
|-----------|-------------|------------------|--------------|
| Qwen3 Coder | 84 | ❌ Failed | Rate-limited (429) - transient |
| Pareto Code Router | 79 | ❌ Failed | Payment required (402) - not free |
| KAT-Coder-Pro V2 | 79 | ❌ Failed | Payment required (402) - not free |

## Detailed Assessment

**Qwen3 Coder 480B A35B (qwen/qwen3-coder:free)**
- ✅ **Strengths**: Highest score (84), appears to be genuinely free-tier, 429 error indicates model exists and is accessible when rate-limited
- ❌ **Weaknesses**: Currently rate-limited, license needs verification
- ⚠️ **Risks**: Provider rate-limit volatility, temporary unavailability

**Pareto Code Router & KAT-Coder-Pro V2**
- ❌ **Major Issue**: Both returned 402 "payment required" errors, indicating they're **not actually free-tier** despite being listed as candidates
- These should be reconsidered only if budget is available

## Recommendation

**TEST_FIRST: Qwen3 Coder 480B A35B**

Despite the current rate-limit, this is the only candidate that:
1. Actually provides free-tier access (the 429 confirms the endpoint exists)
2. Has the highest overall score
3. Shows transient rather than fundamental access issues

**REJECT: Pareto Code Router and KAT-Coder-Pro V2** - These require payment and don't meet the free-tier requirement.

**Human Actions Needed:**
1. Retry Qwen3 Coder after the rate-limit period (14 seconds per error)
2. Verify the Qwen license before production use
3. Consider adding your own API key to OpenRouter to bypass rate limits if the model proves valuable

```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text

## Final Human Approval Summary

### 1. Coding Recommendation
**TEST_FIRST: Qwen3 Coder 480B A35B**
- Highest scoring candidate (84) with genuine free-tier access
- 429 rate-limit error confirms endpoint accessibility (transient issue)
- **REJECT**: Pareto Code Router and KAT-Coder-Pro V2 (require payment)

### 2. Research Recommendation
**REJECT: Baidu Qianfan: CoBuddy**
- Invalid model ID error (400) - configuration issue
- Requires verification of correct model identifier

### 3. Risks
- **Qwen3 Coder**: Provider rate-limit volatility may cause temporary unavailability
- **License verification needed** before production use
- **Research model**: Invalid model ID requires correction

### 4. Final Decision Suggestion
**TEST_FIRST**

**Rationale**: Qwen3 Coder is the only viable free-tier candidate with the highest score. Proceed with retry after rate-limit period and license verification.

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

I'll break down the comparison between open-source and closed-source AI models for you:

## Open-Source AI Models

**Strengths:**
1. **Transparency & Control** - You can inspect, modify, and audit the code and architecture, giving you full understanding of how decisions are made
2. **Community Innovation** - Large collaborative communities continuously improve and adapt models for diverse use cases
3. **Cost-Effective** - Generally free to use and modify, making AI accessible to startups, researchers, and individuals

**Weaknesses:**
1. **Resource Limitations** - Often developed by smaller teams with less computational power and data than big tech companies
2. **Performance Gaps** - May lag behind proprietary models in handling complex, nuanced tasks
3. **Support Challenges** - Limited formal support channels and documentation compared to commercial solutions

## Closed-Source AI Models

**Strengths:**
1. **Advanced Capabilities** - Typically backed by massive resources, resulting in 
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

Looking at these candidates, I need to analyze both the scores and the actual benchmark results to make a recommendation.

## Analysis Summary

| Candidate | Total Score | Benchmark Result | Actual Issue |
|-----------|-------------|------------------|--------------|
| Qwen3 Coder | 84 | ❌ Failed | Rate-limited (429) - transient |
| Pareto Code Router | 79 | ❌ Failed | Payment required (402) - not free |
| KAT-Coder-Pro V2 | 79 | ❌ Failed | Payment required (402) - not free |

## Detailed Assessment

**Qwen3 Coder 480B A35B (qwen/qwen3-coder:free)**
- ✅ **Strengths**: Highest score (84), appears to be genuinely free-tier, 429 error indicates model exists and is accessible when rate-limited
- ❌ **Weaknesses**: Currently rate-limited, license needs verification
- ⚠️ **Risks**: Provider rate-limit volatility, temporary unavailability

**Pareto Code Router & KAT-Coder-Pro V2**
- ❌ **Major Issue**: Both returned 402 "payment required" errors, indicating they're **not actually free-tier** despite being listed as candidates
- These should be reconsidered only if budget is available

## Recommendation

**TEST_FIRST: Qwen3 Coder 480B A35B**

Despite the current rate-limit, this is the only candidate that:
1. Actually provides free-tier access (the 429 confirms the endpoint exists)
2. Has the highest overall score
3. Shows transient rather than fundamental access issues

**REJECT: Pareto Code Router and KAT-Coder-Pro V2** - These require payment and don't meet the free-tier requirement.

**Human Actions Needed:**
1. Retry Qwen3 Coder after the rate-limit period (14 seconds per error)
2. Verify the Qwen license before production use
3. Consider adding your own API key to OpenRouter to bypass rate limits if the model proves valuable

```

### research_review
```text
{"error":{"message":"Baidu Qianfan: CoBuddy (free) is not a valid model ID","code":400},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text

## Final Human Approval Summary

### 1. Coding Recommendation
**TEST_FIRST: Qwen3 Coder 480B A35B**
- Highest scoring candidate (84) with genuine free-tier access
- 429 rate-limit error confirms endpoint accessibility (transient issue)
- **REJECT**: Pareto Code Router and KAT-Coder-Pro V2 (require payment)

### 2. Research Recommendation
**REJECT: Baidu Qianfan: CoBuddy**
- Invalid model ID error (400) - configuration issue
- Requires verification of correct model identifier

### 3. Risks
- **Qwen3 Coder**: Provider rate-limit volatility may cause temporary unavailability
- **License verification needed** before production use
- **Research model**: Invalid model ID requires correction

### 4. Final Decision Suggestion
**TEST_FIRST**

**Rationale**: Qwen3 Coder is the only viable free-tier candidate with the highest score. Proceed with retry after rate-limit period and license verification.

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
