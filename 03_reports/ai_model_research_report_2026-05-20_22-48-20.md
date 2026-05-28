# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-20T22:48:20

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
**Best Candidate**: **Qwen: Qwen3 Coder 480B A35B (free)**  

### Strengths:
- Highest total score (84) and quality metrics (30/30).
- Labeled as "free" (free-tier score: 15/15), though verification needed.
- API-accessible and designed for dynamic evaluation.

### Weaknesses:
- License status unverified (risk of restrictive terms).
- Benchmark failed due to rate-limiting (upstream provider issue).
- Stability concerns (risk of rate-limit changes).

### Risks:
- **Provider/rate-limit changes**: May disrupt access.  
- **License uncertainty**: Could limit commercial/research use.  
- **Benchmark failure**: Current reliability unknown.  

### Recommendation:  
**TEST_FIRST**  
- **Why**: Highest score and free-tier potential, but benchmark failed and license unverified.  
- **Action**: Retry testing Qwen with adjusted token limits; verify license and free-tier status.  

**Other Candidates**:  
- **Pareto Code Router** & **Kwaipilot**: Failed benchmarks due to insufficient credits (free-tier unclear), lower scores (79). **Test only if Qwen fails.**
```

### research_review
```text
# Model Candidate Review

## Summary

Both candidates have **identical profiles** (total_score: 94) with the same strengths, weaknesses, and risk factors. They are essentially "live discovered" models requiring verification.

---

## Candidate 1: Baidu Qianfan: CoBuddy (free)

| Attribute | Assessment |
|-----------|------------|
| **Quality Score** | 30 |
| **Free Tier** | 15 |
| **API** | 15 |
| **Open Source** | 10 |
| **Stability** | 7 |
| **Migration** | 7 |
| **Total** | 94 |

### Strengths
- Live discovered model via OpenRouter API
- Candidate for testing

### Weaknesses
- License must be verified
- Availability may change
- Needs benchmark testing

### Risks
- Provider/rate-limit changes (Baidu)
- Chinese provider may have regulatory concerns

---

## Candidate 2: NVIDIA: Nemotron 3 Nano Omni (free)

| Attribute | Assessment |
|-----------|------------|
| **Quality Score** | 30 |
| **Free Tier** | 15 |
| **API** | 15 |
| **Open Source** | 10 |
| **Stability** | 7 |
| **Migration** | 7 |
| **Total** | 94 |

### Strengths
- Live discovered model via OpenRouter API
- Candidate for testing
- Backed by NVIDIA (established company)

### Weaknesses
- License must be verified
- Availability may change
- Needs benchmark testing

### Risks
- Provider/rate-limit changes

---

## Recommendation

### **TEST_FIRST** for both candidates, but prioritize **NVIDIA Nemotron 3 Nano Omni**

**Rationale:**
1. **Provider stability**: NVIDIA is a more established, Western provider with likely better long-term stability than Baidu
2. **Both require verification**: Neither has verified open-source status or confirmed free-tier availability
3. **Identical scores**: The data shows no meaningful differentiation between them
4. **Risk mitigation**: Testing both in parallel would provide comparative data

### Human Action Required
- ✅ Verify open-source license for both models
- ✅ Confirm free-tier availability on OpenRouter
- ✅ Run benchmark tests to validate research/reasoning capabilities
- ✅ Check rate-limit terms before production use

---

## Final Decision

| Candidate | Decision | Priority |
|-----------|----------|----------|
| NVIDIA Nemotron 3 Nano Omni | TEST_FIRST | High |
| Baidu CoBuddy | TEST_FIRST | Medium |

Both should be tested, but NVIDIA should be evaluated first due to provider reliability.
```

### final_review
```text
**1. Coding recommendation**  
- **Model**: Qwen3 Coder 480B A35B (free)  
- **Strengths**: highest total score (84), top quality metrics (30/30), free‑tier score 15/15, API‑accessible, strong quality metrics.  
- **Weaknesses**: benchmark failed due to rate‑limit issue, license status unverified, risk of provider rate‑limit changes, potential license restrictions limiting commercial/research use.  
- **Risks**: provider rate‑limit changes, license restrictions limiting use, unreliable benchmark results.  
- **Recommendation**: **TEST_FIRST** after verifying license and free‑tier status (retry with lower token limits if needed).

**2. Research recommendation**  
- **Models**: NVIDIA Nemotron 3 Nano Omni (free) and Baidu CoBuddy (free).  
- **Strengths**: identical high scores (94), free‑tier eligibility, API access, strong quality scores, NVIDIA’s stable provider reputation.  
- **Weaknesses**: license verification required, possible availability changes, need for benchmark testing.  
- **Risks**: provider rate‑limit changes, license restrictions, unreliable benchmark results.  
- **Recommendation**: **TEST_FIRST**, prioritize NVIDIA Nemotron 3 Nano Omni (due to provider stability), then Qwen, then Baidu CoBuddy.

**Final decision suggestion**: **TEST_FIRST** (prioritize NVIDIA Nemotron 3 Nano Omni, then Qwen, then other candidates). Not automatic approval; human verification required.
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

# Open-Source vs. Closed-Source AI Models

## Open-Source AI Models

**Strengths:**
1. **Transparency & Auditability** - Code, architecture, and training processes are publicly visible, allowing for security auditing and trust verification
2. **Customization & Control** - Can be freely modified, fine-tuned, and deployed on-premises for specific use cases without vendor lock-in
3. **Cost-Effective** - Typically free to use and distribute, with no ongoing licensing fees or API costs

**Weaknesses:**
1. **Performance Gap** - Generally less capable than cutting-edge closed models, especially in complex reasoning tasks
2. **Resource Intensive** - Require significant computational resources (GPUs) and technical expertise to run effectively
3. **Limited Support** - Rely on community forums rather than professional support teams for troubleshooting

---

## Closed-Source AI Models

**Strengths:**
1. **State-of-the-Art Performance** - Typically more advanced, with better reasoning, multilingua
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
**Best Candidate**: **Qwen: Qwen3 Coder 480B A35B (free)**  

### Strengths:
- Highest total score (84) and quality metrics (30/30).
- Labeled as "free" (free-tier score: 15/15), though verification needed.
- API-accessible and designed for dynamic evaluation.

### Weaknesses:
- License status unverified (risk of restrictive terms).
- Benchmark failed due to rate-limiting (upstream provider issue).
- Stability concerns (risk of rate-limit changes).

### Risks:
- **Provider/rate-limit changes**: May disrupt access.  
- **License uncertainty**: Could limit commercial/research use.  
- **Benchmark failure**: Current reliability unknown.  

### Recommendation:  
**TEST_FIRST**  
- **Why**: Highest score and free-tier potential, but benchmark failed and license unverified.  
- **Action**: Retry testing Qwen with adjusted token limits; verify license and free-tier status.  

**Other Candidates**:  
- **Pareto Code Router** & **Kwaipilot**: Failed benchmarks due to insufficient credits (free-tier unclear), lower scores (79). **Test only if Qwen fails.**
```

### research_review
```text
# Model Candidate Review

## Summary

Both candidates have **identical profiles** (total_score: 94) with the same strengths, weaknesses, and risk factors. They are essentially "live discovered" models requiring verification.

---

## Candidate 1: Baidu Qianfan: CoBuddy (free)

| Attribute | Assessment |
|-----------|------------|
| **Quality Score** | 30 |
| **Free Tier** | 15 |
| **API** | 15 |
| **Open Source** | 10 |
| **Stability** | 7 |
| **Migration** | 7 |
| **Total** | 94 |

### Strengths
- Live discovered model via OpenRouter API
- Candidate for testing

### Weaknesses
- License must be verified
- Availability may change
- Needs benchmark testing

### Risks
- Provider/rate-limit changes (Baidu)
- Chinese provider may have regulatory concerns

---

## Candidate 2: NVIDIA: Nemotron 3 Nano Omni (free)

| Attribute | Assessment |
|-----------|------------|
| **Quality Score** | 30 |
| **Free Tier** | 15 |
| **API** | 15 |
| **Open Source** | 10 |
| **Stability** | 7 |
| **Migration** | 7 |
| **Total** | 94 |

### Strengths
- Live discovered model via OpenRouter API
- Candidate for testing
- Backed by NVIDIA (established company)

### Weaknesses
- License must be verified
- Availability may change
- Needs benchmark testing

### Risks
- Provider/rate-limit changes

---

## Recommendation

### **TEST_FIRST** for both candidates, but prioritize **NVIDIA Nemotron 3 Nano Omni**

**Rationale:**
1. **Provider stability**: NVIDIA is a more established, Western provider with likely better long-term stability than Baidu
2. **Both require verification**: Neither has verified open-source status or confirmed free-tier availability
3. **Identical scores**: The data shows no meaningful differentiation between them
4. **Risk mitigation**: Testing both in parallel would provide comparative data

### Human Action Required
- ✅ Verify open-source license for both models
- ✅ Confirm free-tier availability on OpenRouter
- ✅ Run benchmark tests to validate research/reasoning capabilities
- ✅ Check rate-limit terms before production use

---

## Final Decision

| Candidate | Decision | Priority |
|-----------|----------|----------|
| NVIDIA Nemotron 3 Nano Omni | TEST_FIRST | High |
| Baidu CoBuddy | TEST_FIRST | Medium |

Both should be tested, but NVIDIA should be evaluated first due to provider reliability.
```

### final_review
```text
**1. Coding recommendation**  
- **Model**: Qwen3 Coder 480B A35B (free)  
- **Strengths**: highest total score (84), top quality metrics (30/30), free‑tier score 15/15, API‑accessible, strong quality metrics.  
- **Weaknesses**: benchmark failed due to rate‑limit issue, license status unverified, risk of provider rate‑limit changes, potential license restrictions limiting commercial/research use.  
- **Risks**: provider rate‑limit changes, license restrictions limiting use, unreliable benchmark results.  
- **Recommendation**: **TEST_FIRST** after verifying license and free‑tier status (retry with lower token limits if needed).

**2. Research recommendation**  
- **Models**: NVIDIA Nemotron 3 Nano Omni (free) and Baidu CoBuddy (free).  
- **Strengths**: identical high scores (94), free‑tier eligibility, API access, strong quality scores, NVIDIA’s stable provider reputation.  
- **Weaknesses**: license verification required, possible availability changes, need for benchmark testing.  
- **Risks**: provider rate‑limit changes, license restrictions, unreliable benchmark results.  
- **Recommendation**: **TEST_FIRST**, prioritize NVIDIA Nemotron 3 Nano Omni (due to provider stability), then Qwen, then Baidu CoBuddy.

**Final decision suggestion**: **TEST_FIRST** (prioritize NVIDIA Nemotron 3 Nano Omni, then Qwen, then other candidates). Not automatic approval; human verification required.
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
