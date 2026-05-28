# AI Open-source / Free-tier Model Research Report

Generated at: 2026-05-25T11:30:30

## Executive Summary

This MVP report compares candidate AI models/tools against the current baseline. No replacement is performed automatically.

## Category: coding_analysis

| Rank | Model | Provider | Score | Recommendation Style |
|---:|---|---|---:|---|
| 1 | Qwen Coder family | OpenRouter / Hugging Face / local | 78 | Candidate |
| 2 | StarCoder / BigCode family | Hugging Face / local | 77 | Candidate |
| 3 | DeepSeek Coder / DeepSeek reasoning-coder variants | OpenRouter / provider API / local where available | 75 | Candidate |

### Qwen Coder family
- Provider: OpenRouter / Hugging Face / local
- Open-source status: open-weight family, verify license per exact model
- Free-tier/API status: may be available via free/provider tiers; verify during live run
- Best use case: coding assistant, refactor, code explanation
- Risk: provider/rate-limit changes
- Migration difficulty: medium
### DeepSeek Coder / DeepSeek reasoning-coder variants
- Provider: OpenRouter / provider API / local where available
- Open-source status: verify exact model/license
- Free-tier/API status: verify current API availability
- Best use case: debugging and code reasoning
- Risk: API/provider changes
- Migration difficulty: medium
### StarCoder / BigCode family
- Provider: Hugging Face / local
- Open-source status: open model family, verify exact version/license
- Free-tier/API status: can be tested through HF/local depending on size
- Best use case: open-source coding baseline
- Risk: quality gap versus newer models
- Migration difficulty: low-medium
## Category: research_reasoning

| Rank | Model | Provider | Score | Recommendation Style |
|---:|---|---|---:|---|
| 1 | DeepSeek R1 family | OpenRouter / Hugging Face / provider API | 79 | Candidate |
| 2 | Llama instruct family | Groq / OpenRouter / Hugging Face / local | 79 | Candidate |
| 3 | Qwen reasoning/instruct family | OpenRouter / Hugging Face / local | 78 | Candidate |

### DeepSeek R1 family
- Provider: OpenRouter / Hugging Face / provider API
- Open-source status: open-weight family, verify exact model/license
- Free-tier/API status: verify current free/provider tier
- Best use case: reasoning-heavy research analysis
- Risk: hallucination if not source-grounded
- Migration difficulty: medium
### Qwen reasoning/instruct family
- Provider: OpenRouter / Hugging Face / local
- Open-source status: open-weight family, verify exact model/license
- Free-tier/API status: verify current free/provider tier
- Best use case: research summary and bilingual analysis
- Risk: model/version fragmentation
- Migration difficulty: medium
### Llama instruct family
- Provider: Groq / OpenRouter / Hugging Face / local
- Open-source status: open-weight family, verify license per version
- Free-tier/API status: often available through providers; verify live
- Best use case: general research and summary baseline
- Risk: quality depends heavily on model size/provider
- Migration difficulty: low-medium
## Final Recommendation

### coding_analysis
- Current baseline score: 70
- Best candidate: Qwen Coder family
- Best candidate score: 78
- Improvement: 11.43%
- Decision: TEST_FIRST

### research_reasoning
- Current baseline score: 70
- Best candidate: DeepSeek R1 family
- Best candidate score: 79
- Improvement: 12.86%
- Decision: TEST_FIRST

## Human Approval

Choose one:
- APPROVE
- REJECT
- TEST_FIRST

No system change should happen until human decision is recorded.
