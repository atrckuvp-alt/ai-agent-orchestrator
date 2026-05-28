# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-20T23:34:42

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
{"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1779321600000"},"provider_name":null}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### research_review
```text
{"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1779321600000"},"provider_name":null}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text
'choices'
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

### **Open-Source AI Models**  
**Strengths:**  
1. **Transparency & Trust**: Source code and training data are publicly accessible, allowing scrutiny for biases, security, or ethical concerns.  
2. **Flexibility & Customization**: Developers can modify, fine-tune, or integrate models into specific use cases without licensing restrictions.  
3. **Community Innovation**: Large collaborative communities drive rapid iteration, shared improvements, and cost-effective development.  

**Weaknesses:**  
1. **Inconsistent Quality**: Variability in contributions can lead to bugs, outdated versions, or unmaintained projects.  
2. **Limited Resources**: May lack the computational power, datasets, or expertise of big tech companies, resulting in lower performance.  
3. **Support Challenges**: Reliance on community-driven support, which may be slow or unavailable for critical issues.  

---

### **Closed-Source AI Models**  
**Strengths:**  
1. **High Performance**: Backed by massive resources, le
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
{"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1779321600000"},"provider_name":null}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### research_review
```text
{"error":{"message":"Rate limit exceeded: free-models-per-day. Add 10 credits to unlock 1000 free model requests per day","code":429,"metadata":{"headers":{"X-RateLimit-Limit":"50","X-RateLimit-Remaining":"0","X-RateLimit-Reset":"1779321600000"},"provider_name":null}},"user_id":"user_3DwvHydeNrDpCeQHaaFQqY8fBNH"}
```

### final_review
```text
'choices'
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
