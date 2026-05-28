"""
AI Agent Research Team MVP v1

Run:
    python 04_scripts/run_orchestrator.py --mock

Optional real API mode:
    set OPENROUTER_API_KEY=your_key_here
    python 04_scripts/run_orchestrator.py --api openrouter

This MVP is intentionally safe:
- It does not auto-replace any model.
- It writes an approval request only.
- Human must approve manually.
"""

import argparse
import datetime as dt
import json
import os

import requests
from dotenv import load_dotenv

from pathlib import Path
from typing import Dict, Any, List

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "00_memory"
REPORTS = ROOT / "03_reports"

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def score_model(model: Dict[str, Any]) -> int:
    weights = {
        "quality": 30,
        "free_tier": 20,
        "api": 15,
        "open_source": 15,
        "stability": 10,
        "migration": 10,
    }
    total = 0
    for key, weight in weights.items():
        total += min(max(int(model.get("scores", {}).get(key, 0)), 0), weight)
    return total

def fetch_openrouter_models():
    data = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
        },
        timeout=30
    ).json()

    candidates = []

    for model in data.get("data", []):
        model_id = model.get("id", "")
        name = model.get("name", model_id)
        lower = (model_id + " " + name).lower()

        category = "research_reasoning"
        if "code" in lower or "coder" in lower:
            category = "coding_analysis"

        item = {
            "name": name,
            "model_id": model_id,
            "provider": "OpenRouter",
            "category": category,
            "open_source_status": "verify exact license",
            "free_tier_status": "verify current free-tier",
            "strengths": ["live discovered model", "available via API", "candidate for testing"],
            "weaknesses": ["license must be verified", "availability may change", "needs benchmark testing"],
            "best_use_case": "dynamic evaluation",
            "risk": "provider/rate-limit changes",
            "migration_difficulty": "medium",
            "scores": {
                "quality": 30,
                "free_tier": 15 if "free" in lower else 10,
                "api": 15,
                "open_source": 10,
                "stability": 7,
                "migration": 7
            }
        }

        item["total_score"] = score_model(item)
        candidates.append(item)

    coding = sorted(
        [m for m in candidates if m["category"] == "coding_analysis"],
        key=lambda x: x["total_score"],
        reverse=True
    )[:3]

    research = sorted(
        [m for m in candidates if m["category"] == "research_reasoning"],
        key=lambda x: x["total_score"],
        reverse=True
    )[:3]

    return {
        "coding_analysis": coding,
        "research_reasoning": research
    }

def estimate_task_complexity(task_prompt: str) -> str:
    """วิเคราะห์ความซับซ้อนของงานจาก task prompt"""
    if not task_prompt:
        return "cheap"
    
    prompt_length = len(task_prompt)
    
    if prompt_length < 300:
        return "cheap"
    elif prompt_length < 1000:
        return "normal"
    else:
        return "reasoning"

def choose_model_for_task(agent_name, task_prompt=None, task_complexity="normal"):
    """
    เลือกโมเดลอัจฉริยะ โดยพิจารณา Task Complexity + Model Health
    """
    # วิเคราะห์ความซับซ้อนของงาน
    if task_prompt:
        task_complexity = estimate_task_complexity(task_prompt)

    # ใช้ Smart Model Selector ถ้ามีข้อมูล health
    health_path = MEMORY / "model_health.json"
    if health_path.exists():
        return get_smart_model_selection(agent_name, task_complexity)
    
    # Fallback ไปใช้ logic เดิม
    model_costs_path = MEMORY / "model_costs.json"
    try:
        model_costs = load_json(model_costs_path)
    except:
        model_costs = {}

    runtime_path = MEMORY / "agent_runtime_config.json"
    runtime_config = load_json(runtime_path)

    default_model = runtime_config.get(
        agent_name, {}
    ).get("model", "openrouter/free")

    if task_complexity == "cheap":
        return "openrouter/free"

    if task_complexity == "reasoning" and agent_name == "research_agent":
        return runtime_config.get("research_agent", {}).get("model", default_model)

    return default_model

def call_openrouter_model(model_id, prompt):

    api_key = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        return {
            "success": False,
            "error": response.text
        }

    data = response.json()

    try:
        text = data["choices"][0]["message"]["content"]

        return {
            "success": True,
            "content": text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def is_bad_response(result: dict) -> bool:
    """ตรวจสอบว่าผลลัพธ์มีปัญหา (สำหรับ fallback)"""
    if not result or not result.get("success"):
        return True
    
    content = result.get("content", "").strip()
    if not content or len(content) < 15:
        return True
    
    # ตรวจคำที่บ่งชี้การปฏิเสธหรือ hallucination
    bad_phrases = [
        "i don't know", "as an ai", "cannot access", "sorry i cannot", 
        "i am unable", "no information", "cannot provide", "i cannot"
    ]
    if any(phrase in content.lower() for phrase in bad_phrases):
        return True
    
    return False

def get_fallback_models(agent_name: str, primary_model: str) -> list:
    """โหลดลำดับ fallback models จากไฟล์"""
    fallback_path = MEMORY / "fallback_models.json"
    
    try:
        fallback_config = load_json(fallback_path)
    except:
        fallback_config = {"default": ["openrouter/free"]}
    
    # หาลำดับ fallback ตาม agent
    agent_fallbacks = fallback_config.get(agent_name, fallback_config.get("default", []))
    
# ลบ primary_model ออกเพื่อไม่ให้วน loop
    fallbacks = [m for m in agent_fallbacks if m != primary_model]
    
    return fallbacks if fallbacks else ["openrouter/free"]

def call_model_with_fallback(agent_name: str, model_id: str, prompt: str, max_fallbacks=2):
    """Intelligent Fallback Routing"""
    attempted_models = []
    current_model = model_id

    for attempt in range(max_fallbacks + 1):
        attempted_models.append(current_model)
        
        print(f"Attempt {attempt+1}/{max_fallbacks+1} | {agent_name} | Model: {current_model}")
        
        result = call_openrouter_model(current_model, prompt)
        
        if result.get("success") and not is_bad_response(result):
            if attempt > 0:
                print(f"✅ Fallback successful → {current_model}")
            return result, current_model, attempted_models
        
        print(f"⚠️ Failed: {current_model}")
        
        fallbacks = get_fallback_models(agent_name, current_model)
        if not fallbacks:
            break
        current_model = fallbacks[0]

    print(f"❌ All fallback models failed for {agent_name}")
    return {
        "success": False,
        "error": "All fallback models exhausted",
        "attempted_models": attempted_models
    }, current_model, attempted_models

def update_model_health(model_id: str, success: bool, duration: float, result=None):
    """อัพเดทสถิติสุขภาพของโมเดล"""
    health_path = MEMORY / "model_health.json"
    
    if health_path.exists():
        model_health = load_json(health_path)
    else:
        model_health = {"models": {}, "last_updated": None}
    
    if model_id not in model_health["models"]:
        model_health["models"][model_id] = {
            "success_count": 0,
            "failure_count": 0,
            "total_duration": 0.0,
            "avg_latency": 0.0,
            "failure_rate": 0.0,
            "last_used": None,
            "status": "active"
        }
    
    health = model_health["models"][model_id]
    health["last_used"] = dt.datetime.now().isoformat()
    
    if success:
        health["success_count"] += 1
    else:
        health["failure_count"] += 1
    
    health["total_duration"] += duration
    health["avg_latency"] = health["total_duration"] / (health["success_count"] + health["failure_count"])
    health["failure_rate"] = health["failure_count"] / (health["success_count"] + health["failure_count"]) if (health["success_count"] + health["failure_count"]) > 0 else 0
    
    model_health["last_updated"] = dt.datetime.now().isoformat()
    
    save_json(health_path, model_health)
    return health

def get_smart_model_selection(agent_name: str, task_complexity="normal"):
    """
    Smart Model Selector - พิจารณา Speed, Quality, Cost, Failure Rate
    """
    health_path = MEMORY / "model_health.json"
    
    try:
        model_health = load_json(health_path)
    except:
        model_health = {"models": {}}
    
    # โหลด fallback models
    fallback_path = MEMORY / "fallback_models.json"
    try:
        fallback_config = load_json(fallback_path)
    except:
        fallback_config = {}
    
    candidates = fallback_config.get(agent_name, fallback_config.get("default", ["openrouter/free"]))
    
    best_score = -1
    best_model = "openrouter/free"
    
    for model_id in candidates:
        health = model_health["models"].get(model_id, {})
        
        success_rate = 1 - health.get("failure_rate", 0.3)
        avg_latency = health.get("avg_latency", 15.0)
        quality = health.get("quality_score", 5.0)
        
        # คะแนนรวม (ปรับน้ำหนักได้)
        score = (
            success_rate * 0.4 +           # Success Rate 40%
            (1 / (avg_latency + 1)) * 0.25 +  # Latency 25%
            quality * 0.25 +               # Quality 25%
            (10 if "free" in model_id else 5) * 0.1   # Cost 10%
        )
        
        if score > best_score:
            best_score = score
            best_model = model_id
    
    print(f"🤖 Smart Selector → {agent_name} chose: {best_model} (score: {best_score:.3f})")
    return best_model

def analyze_system_performance(runtime_metrics, model_health):
    """Autonomous Runtime Intelligence Analyzer - เวอร์ชันปรับปรุง"""
    suggestions = []
    
    if not runtime_metrics or not runtime_metrics.get("runs"):
        return suggestions

    runs = runtime_metrics["runs"][-100:]  # วิเคราะห์ 100 รันล่าสุด

    # 1. วิเคราะห์ตามโมเดล
    from collections import defaultdict
    model_stats = defaultdict(lambda: {
        "success": 0, "fail": 0, "total_time": 0.0, 
        "fallback_count": 0, "count": 0
    })

    for run in runs:
        model = run.get("used_model")
        success = run.get("success", False)
        duration = run.get("duration_seconds", 0)
        fallback_used = run.get("fallback_used", False)
        
        model_stats[model]["count"] += 1
        model_stats[model]["total_time"] += duration
        if success:
            model_stats[model]["success"] += 1
        else:
            model_stats[model]["fail"] += 1
        if fallback_used:
            model_stats[model]["fallback_count"] += 1

    # 2. สร้างข้อเสนอแนะอัจฉริยะ
    for model, stats in model_stats.items():
        if stats["count"] == 0:
            continue
            
        success_rate = stats["success"] / stats["count"]
        avg_latency = stats["total_time"] / stats["count"]
        fallback_rate = stats["fallback_count"] / stats["count"]

        # Reliability Issue
        if success_rate < 0.8:
            suggestions.append({
                "timestamp": dt.datetime.now().isoformat(),
                "type": "reliability",
                "target": model,
                "severity": "high",
                "issue": f"{model} มี Failure Rate สูง ({(1-success_rate)*100:.1f}%)",
                "suggestion": f"ลด priority ของ {model} หรือเพิ่ม fallback models เพิ่มเติม",
                "priority": "high"
            })

        # Latency Issue
        if avg_latency > 20:
            suggestions.append({
                "timestamp": dt.datetime.now().isoformat(),
                "type": "latency",
                "target": model,
                "severity": "medium",
                "issue": f"{model} ช้าเฉลี่ย {avg_latency:.2f} วินาที",
                "suggestion": f"ใช้โมเดลที่เร็วขึ้นสำหรับ task ระดับ cheap/normal",
                "priority": "medium"
            })

        # Fallback Issue
        if fallback_rate > 0.3:
            suggestions.append({
                "timestamp": dt.datetime.now().isoformat(),
                "type": "fallback",
                "target": model,
                "severity": "high",
                "issue": f"{model} ต้อง fallback บ่อย ({fallback_rate*100:.1f}%)",
                "suggestion": f"ตรวจสอบ API Key / Rate Limit หรือเปลี่ยน primary model",
                "priority": "high"
            })

    # 3. ข้อเสนอระดับระบบ
    total_runs = len(runs)
    if total_runs > 15:
        suggestions.append({
            "timestamp": dt.datetime.now().isoformat(),
            "type": "system",
            "issue": f"ระบบรันมาแล้ว {total_runs} ครั้ง",
            "suggestion": "พิจารณาปรับน้ำหนักใน get_smart_model_selection ให้เรียนรู้จาก failure_rate และ latency",
            "priority": "low"
        })

    return suggestions

def apply_self_optimization(self_improvement_log, model_health):
    """ปรับน้ำหนักระบบอัตโนมัติตามการวิเคราะห์"""
    if not self_improvement_log.get("suggestions"):
        return False

    optimized = False
    high_priority = [s for s in self_improvement_log["suggestions"] if s.get("priority") == "high"]

    for sug in high_priority[-5:]:  # 5 ข้อล่าสุด
        target = sug.get("target")
        if not target or target == "System":
            continue

        if target not in model_health.get("models", {}):
            continue

        health = model_health["models"][target]
        
        # ปรับตามปัญหา
        if sug.get("type") == "reliability" and health.get("failure_rate", 0) > 0.25:
            # ลดคะแนนโมเดลที่ fail บ่อย
            health["quality_score"] = health.get("quality_score", 5) - 2
            print(f"🔧 Auto-Optimize: ลด quality score ของ {target} เนื่องจาก fail บ่อย")
            optimized = True

        elif sug.get("type") == "latency" and health.get("avg_latency", 0) > 25:
            health["quality_score"] = health.get("quality_score", 5) - 1.5
            print(f"🔧 Auto-Optimize: ลดคะแนน {target} เนื่องจาก latency สูง")
            optimized = True

    if optimized:
        # บันทึกการปรับเปลี่ยน
        if "optimization_history" not in self_improvement_log:
            self_improvement_log["optimization_history"] = []
        
        self_improvement_log["optimization_history"].append({
            "timestamp": dt.datetime.now().isoformat(),
            "action": "dynamic_weight_adjustment",
            "affected_models": [s.get("target") for s in high_priority[-5:]],
            "note": "ปรับตาม Self-Analysis"
        })

    return optimized

def run_agent(agent_name, model_id, task_prompt, runtime_metrics, runtime_metrics_path):
    print(f"Running agent: {agent_name} with primary model: {model_id}")

    start_time = dt.datetime.now()

    system_prompt = f"""
You are {agent_name}.
You are part of an AI model research team.

Rules:
- Prefer open-source models.
- Prefer free-tier or free API models.
- Be concise.
- Always mention strengths, weaknesses, and risks.
- Never recommend replacement without human approval.
"""

    full_prompt = system_prompt + "\n\nTask:\n" + task_prompt

    # === Intelligent Fallback Routing ===
    result, used_model, attempted_models = call_model_with_fallback(
        agent_name, model_id, full_prompt, max_fallbacks=2
    )

    end_time = dt.datetime.now()
    duration = (end_time - start_time).total_seconds()

    # === Update Model Health ===
    update_model_health(used_model, result.get("success", False), duration, result)

    # บันทึก runtime metrics
    runtime_metrics["runs"].append({
        "timestamp": end_time.isoformat(),
        "agent": agent_name,
        "original_model": model_id,
        "used_model": used_model,
        "fallback_used": used_model != model_id,
        "attempted_models": attempted_models,
        "duration_seconds": duration,
        "success": result.get("success", False),
        "error": result.get("error") if not result.get("success") else None
    })

    save_json(runtime_metrics_path, runtime_metrics)

    print(f"{agent_name} finished in {duration:.2f} seconds (used: {used_model})")

    return {
        "agent_name": agent_name,
        "model_id": used_model,
        "original_model": model_id,
        "result": result,
        "fallback_used": used_model != model_id
    }

def run_agent_team_review(candidates, runtime_config, 
                         runtime_metrics, runtime_metrics_path):

    orchestrator_model = runtime_config["orchestrator"]["model"]
    coding_agent_model = runtime_config["coding_agent"]["model"]
    research_agent_model = runtime_config["research_agent"]["model"]

    coding_summary = json.dumps(
        candidates.get("coding_analysis", []), 
        ensure_ascii=False, indent=2
    )[:6000]

    research_summary = json.dumps(
        candidates.get("research_reasoning", []), 
        ensure_ascii=False, indent=2
    )[:6000]

    # ใช้ task_prompt จริงในการเลือก model
    
    coding_review = run_agent(
        "coding_agent",
        coding_agent_model,
        f"""
Review these coding/analysis model candidates.
Choose the best candidate.
Explain strengths, weaknesses, risks, and whether human should TEST_FIRST or REJECT.

Candidates:
{coding_summary}
""",
        runtime_metrics,        # ← เพิ่ม
        runtime_metrics_path    # ← เพิ่ม
    )

    research_review = run_agent(
        "research_agent",
        research_agent_model,
        f"""
Review these research/reasoning model candidates.
Choose the best candidate.
Explain strengths, weaknesses, risks, and whether human should TEST_FIRST or REJECT.

Candidates:
{research_summary}
""",
        runtime_metrics,        # ← เพิ่ม
        runtime_metrics_path    # ← เพิ่ม
    )

    final_review = run_agent(
        "orchestrator",
        orchestrator_model,
        f"""
You are the orchestrator.
Combine coding agent review and research agent review into final human approval summary.
Do not approve automatically.
Return:
1. Coding recommendation
2. Research recommendation
3. Risks
4. Final decision suggestion: TEST_FIRST / REJECT / KEEP_CURRENT

Coding Review:
{json.dumps(coding_review, ensure_ascii=False, indent=2)[:5000]}

Research Review:
{json.dumps(research_review, ensure_ascii=False, indent=2)[:5000]}
""",
        runtime_metrics,        # ← เพิ่ม
        runtime_metrics_path    # ← เพิ่ม
    )

    return {
        "coding_review": coding_review,
        "research_review": research_review,
        "final_review": final_review
    }

def evaluate_benchmark_quality(result, current_score=0):
    """
    ประเมินคุณภาพ benchmark และตัดสินใจ Rollback / Upgrade
    """
    if not result or not result.get("success"):
        return {"decision": "keep", "score": 0}

    content = result.get("content", "")

    if not content:
        return {"decision": "keep", "score": 1}

    score = 0
    content_length = len(content)

    if content_length > 200:
        score += 3
    if "strength" in content.lower():
        score += 2
    if "weakness" in content.lower():
        score += 2
    if "risk" in content.lower():
        score += 2
    if "recommend" in content.lower():
        score += 1

    # === Auto Rollback Rule ===
    if result.get("score", 0) < 0.5:
        print("🚨 AUTO ROLLBACK TRIGGERED")
        rollback_path = MEMORY / "rollback_history.json"
        
        rollback_memory = load_json(rollback_path)
        # ป้องกัน key error ถ้าไม่มี "rollbacks"
        rollback_memory.setdefault("rollbacks", []).append({
            "timestamp": dt.datetime.now().isoformat(),
            "model": result.get("model"),
            "reason": "benchmark score below threshold",
            "score": result.get("score", 0)
        })
        
        save_json(rollback_path, rollback_memory)
        
        return {
            "decision": "rollback",
            "reason": "low benchmark score",
            "score": score
        }

    # === Upgrade Recommendation ===
    recommendation = "upgrade" if score > current_score else "keep"

    return {
        "decision": recommendation,
        "score": min(score, 10)
    }

def benchmark_models(candidates):

    coding_prompt = """
Write a simple Python function that receives a list of numbers
and returns the average. Include error handling.
"""

    research_prompt = """
Compare open-source AI models and closed-source AI models.
Give 3 strengths and 3 weaknesses of each.
"""

    for category, models in candidates.items():
        for model in models:
            model_id = model.get("model_id")
            if not model_id:
                continue

            prompt = (
                coding_prompt
                if category == "coding_analysis"
                else research_prompt
            )

            result = call_openrouter_model(model_id, prompt)
            model["benchmark"] = result

            if result.get("success"):
                # ใช้ฟังก์ชันใหม่
                quality_result = evaluate_benchmark_quality(result, current_score=5)
                
                model["benchmark_score"] = quality_result["score"]
                model["benchmark_decision"] = quality_result["decision"]
                
                model["total_score"] = (
                    model.get("total_score", 0) + quality_result["score"]
                )
            else:
                model["benchmark_score"] = 0
                model["benchmark_decision"] = "failed"
                model["total_score"] = model.get("total_score", 0)

    return candidates

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"OpenRouter API Error: {response.text}"
        )

    data = response.json()
    raw_models = data.get("data", [])

    candidates = []

    for model in raw_models:

        model_id = model.get("id", "")
        name = model.get("name", model_id)

        lower = (
            model_id.lower()
            + " "
            + name.lower()
        )

        score = 40

        if "coder" in lower or "code" in lower:
            score += 25

        if "deepseek" in lower:
            score += 18

        if "qwen" in lower:
            score += 15

        if "llama" in lower:
            score += 10

        if "mistral" in lower:
            score += 8

        if "free" in lower:
            score += 15

        if "reason" in lower or "r1" in lower:
            score += 15

        category = "research_reasoning"

        if "coder" in lower or "code" in lower:
            category = "coding_analysis"

        item = {
            "name": name,
            "model_id": model_id,
            "provider": "OpenRouter",
            "category": category,
            "open_source_status": "verify exact license",
            "free_tier_status": "verify current free-tier",
            "strengths": [
                "live discovered model",
                "available via API",
                "candidate for testing"
            ],
            "weaknesses": [
                "license must be verified",
                "availability may change",
                "needs benchmark testing"
            ],
            "best_use_case": "dynamic evaluation",
            "risk": "provider/rate-limit changes",
            "migration_difficulty": "medium",
            "scores": {
                "quality": min(score, 30),
                "free_tier": 15 if "free" in lower else 10,
                "api": 15,
                "open_source": 10,
                "stability": 7,
                "migration": 7
            }
        }

        item["total_score"] = score_model(item)

        candidates.append(item)

    coding = [
        m for m in candidates
        if m["category"] == "coding_analysis"
    ]

    research = [
        m for m in candidates
        if m["category"] == "research_reasoning"
    ]

    coding = sorted(
        coding,
        key=lambda x: x["total_score"],
        reverse=True
    )[:3]

    research = sorted(
        research,
        key=lambda x: x["total_score"],
        reverse=True
    )[:3]


    return {
        "coding_analysis": coding,
        "research_reasoning": research
    }

def mock_candidates() -> Dict[str, List[Dict[str, Any]]]:
    coding = [
        {
            "name": "Qwen Coder family",
            "provider": "OpenRouter / Hugging Face / local",
            "category": "coding_analysis",
            "open_source_status": "open-weight family, verify license per exact model",
            "free_tier_status": "may be available via free/provider tiers; verify during live run",
            "strengths": ["strong coding focus", "good multilingual capability", "good candidate for code assistant workflow"],
            "weaknesses": ["free availability can change", "exact license depends on model", "may require routing provider"],
            "best_use_case": "coding assistant, refactor, code explanation",
            "risk": "provider/rate-limit changes",
            "migration_difficulty": "medium",
            "scores": {"quality": 25, "free_tier": 15, "api": 12, "open_source": 12, "stability": 7, "migration": 7}
        },
        {
            "name": "DeepSeek Coder / DeepSeek reasoning-coder variants",
            "provider": "OpenRouter / provider API / local where available",
            "category": "coding_analysis",
            "open_source_status": "verify exact model/license",
            "free_tier_status": "verify current API availability",
            "strengths": ["strong code reasoning", "good debugging potential", "cost-efficient candidate"],
            "weaknesses": ["availability may vary", "some variants may not be fully open-source", "needs benchmark confirmation"],
            "best_use_case": "debugging and code reasoning",
            "risk": "API/provider changes",
            "migration_difficulty": "medium",
            "scores": {"quality": 26, "free_tier": 14, "api": 11, "open_source": 10, "stability": 7, "migration": 7}
        },
        {
            "name": "StarCoder / BigCode family",
            "provider": "Hugging Face / local",
            "category": "coding_analysis",
            "open_source_status": "open model family, verify exact version/license",
            "free_tier_status": "can be tested through HF/local depending on size",
            "strengths": ["designed for code", "open ecosystem", "good for self-hosting tests"],
            "weaknesses": ["may lag newer frontier models", "needs hardware if local", "not always best for reasoning"],
            "best_use_case": "open-source coding baseline",
            "risk": "quality gap versus newer models",
            "migration_difficulty": "low-medium",
            "scores": {"quality": 21, "free_tier": 16, "api": 10, "open_source": 15, "stability": 7, "migration": 8}
        }
    ]

    research = [
        {
            "name": "DeepSeek R1 family",
            "provider": "OpenRouter / Hugging Face / provider API",
            "category": "research_reasoning",
            "open_source_status": "open-weight family, verify exact model/license",
            "free_tier_status": "verify current free/provider tier",
            "strengths": ["strong reasoning", "good analysis workflow", "useful for comparison tasks"],
            "weaknesses": ["can be verbose", "provider availability can change", "needs citation discipline"],
            "best_use_case": "reasoning-heavy research analysis",
            "risk": "hallucination if not source-grounded",
            "migration_difficulty": "medium",
            "scores": {"quality": 27, "free_tier": 14, "api": 12, "open_source": 12, "stability": 7, "migration": 7}
        },
        {
            "name": "Qwen reasoning/instruct family",
            "provider": "OpenRouter / Hugging Face / local",
            "category": "research_reasoning",
            "open_source_status": "open-weight family, verify exact model/license",
            "free_tier_status": "verify current free/provider tier",
            "strengths": ["good general reasoning", "multilingual strength", "strong candidate for Thai/English workflows"],
            "weaknesses": ["exact model matters", "context length varies", "free access may change"],
            "best_use_case": "research summary and bilingual analysis",
            "risk": "model/version fragmentation",
            "migration_difficulty": "medium",
            "scores": {"quality": 25, "free_tier": 15, "api": 12, "open_source": 12, "stability": 7, "migration": 7}
        },
        {
            "name": "Llama instruct family",
            "provider": "Groq / OpenRouter / Hugging Face / local",
            "category": "research_reasoning",
            "open_source_status": "open-weight family, verify license per version",
            "free_tier_status": "often available through providers; verify live",
            "strengths": ["large ecosystem", "many provider options", "good for general summarization"],
            "weaknesses": ["not always best at deep reasoning", "license varies by version", "needs careful prompting"],
            "best_use_case": "general research and summary baseline",
            "risk": "quality depends heavily on model size/provider",
            "migration_difficulty": "low-medium",
            "scores": {"quality": 22, "free_tier": 16, "api": 13, "open_source": 12, "stability": 8, "migration": 8}
        }
    ]

    for m in coding + research:
        m["total_score"] = score_model(m)
    return {"coding_analysis": coding, "research_reasoning": research}

def compare_to_current(current_stack: Dict[str, Any], candidates: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    # Baseline for current manual ChatGPT Plus workflow in this MVP.
    # You can edit this later when you have measured scores.
    current_baseline_score = 70
    recommendations = {}
    for category, items in candidates.items():
        best = max(items, key=lambda x: x["total_score"])
        improvement = ((best["total_score"] - current_baseline_score) / current_baseline_score) * 100
        recommendations[category] = {
            "current_baseline_score": current_baseline_score,
            "best_candidate": best,
            "improvement_percent": round(improvement, 2),
            "decision": "TEST_FIRST" if improvement >= 0 else "KEEP_CURRENT"
        }
        if improvement >= 15:
            recommendations[category]["decision"] = "REPLACE_AFTER_APPROVAL"
    return recommendations

def write_report(candidates, recommendations, agent_team_review=None, self_improvement_log=None):
    now = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = REPORTS / f"ai_model_research_report_{now}.md"

    lines = []
    lines.append("# AI Open-source / Free-tier Model Research Report\n")
    lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}\n")
    lines.append("## Executive Summary\n")
    lines.append("This MVP report compares candidate AI models/tools against the current baseline. No replacement is performed automatically.\n")

    # === ส่วนเดิม (Categories, Models, Agent Review) ===
    for category, items in candidates.items():
        lines.append(f"## Category: {category}\n")
        lines.append("| Rank | Model | Provider | Score | Recommendation Style |")
        lines.append("|---:|---|---|---:|---|")
        for i, m in enumerate(sorted(items, key=lambda x: x["total_score"], reverse=True), 1):
            lines.append(f"| {i} | {m['name']} | {m['provider']} | {m['total_score']} | Candidate |")
        lines.append("")

        for m in items:
            lines.append(f"### {m['name']}")
            lines.append(f"- Provider: {m['provider']}")
            lines.append(f"- Open-source status: {m['open_source_status']}")
            lines.append(f"- Free-tier/API status: {m['free_tier_status']}")
            lines.append(f"- Best use case: {m['best_use_case']}")
            lines.append(f"- Risk: {m['risk']}")
            lines.append(f"- Migration difficulty: {m['migration_difficulty']}")

            if m.get("benchmark"):
                lines.append(f"- Benchmark score: {m.get('benchmark_score', 0)}")
                # ... (ส่วน benchmark เดิม) ...

    if agent_team_review:
        lines.append("## Agent Team Review\n")
        for key, review in agent_team_review.items():
            lines.append(f"### {key}")
            result = review.get("result", {})
            if result.get("success"):
                lines.append("```text")
                lines.append((result.get("content") or "")[:3000])
                lines.append("```")
            else:
                lines.append("```text")
                lines.append(str(result.get("error", "Unknown error")))
                lines.append("```")

    # === Self-Improvement Report ===
    lines.append("\n## 🧠 Self-Improvement Analysis\n")
    if self_improvement_log and self_improvement_log.get("suggestions"):
        suggestions = self_improvement_log["suggestions"][-8:]  # 8 ข้อล่าสุด
        lines.append(f"**พบ {len(suggestions)} ข้อเสนอแนะจากการวิเคราะห์ระบบ**\n")
        
        for i, sug in enumerate(suggestions, 1):
            emoji = "🚨" if sug.get("priority") == "high" else "⚠️"
            lines.append(f"### {emoji} {i}. {sug.get('issue')}")
            lines.append(f"- **Target:** {sug.get('target', 'System')}")
            lines.append(f"- **Suggestion:** {sug.get('suggestion')}")
            lines.append("")
    else:
        lines.append("ยังไม่มีข้อเสนอแนะ ระบบกำลังเรียนรู้...\n")

    # === Final Recommendation ===
    lines.append("## Final Recommendation\n")
    for category, rec in recommendations.items():
        best = rec["best_candidate"]
        lines.append(f"### {category}")
        lines.append(f"- Current baseline score: {rec['current_baseline_score']}")
        lines.append(f"- Best candidate: {best['name']}")
        lines.append(f"- Best candidate score: {best['total_score']}")
        lines.append(f"- Improvement: {rec['improvement_percent']}%")
        lines.append(f"- Decision: {rec['decision']}")
        lines.append("")

    lines.append("## Human Approval\n")
    lines.append("Choose one:")
    lines.append("- APPROVE")
    lines.append("- REJECT")
    lines.append("- TEST_FIRST")
    lines.append("\nNo system change should happen until human decision is recorded.\n")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path

def update_memory(candidates, recommendations, report_path, 
                 runtime_metrics, runtime_metrics_path, 
                 agent_team_review=None):
    
    # === กำหนด Path ทั้งหมด ===
    registry_path = MEMORY / "model_registry.json"
    history_path = MEMORY / "evaluation_history.json"
    approval_path = MEMORY / "approval_queue.json"
    benchmark_path = MEMORY / "benchmark_history.json"
    agent_review_path = MEMORY / "agent_review_history.json"
    champion_path = MEMORY / "champion_models.json"
    decision_path = MEMORY / "decision_history.json"
    self_improvement_path = MEMORY / "self_improvement_log.json"
    fallback_path = MEMORY / "fallback_history.json"
    health_path = MEMORY / "model_health.json"

    # === โหลดไฟล์ทั้งหมดอย่างปลอดภัย ===
    registry = load_json(registry_path)
    history = load_json(history_path)
    approval = load_json(approval_path)
    benchmark_history = load_json(benchmark_path)
    agent_review_history = load_json(agent_review_path)
    champion_models = load_json(champion_path)
    decision_history = load_json(decision_path)
    
    if fallback_path.exists():
        fallback_history = load_json(fallback_path)
    else:
        fallback_history = {"fallbacks": []}

    if health_path.exists():
        model_health = load_json(health_path)
    else:
        model_health = {"models": {}, "last_updated": None}

    # โหลด Self-Improvement Memory
    if self_improvement_path.exists():
        self_improvement_log = load_json(self_improvement_path)
    else:
        self_improvement_log = {"improvements": [], "suggestions": [], "last_analysis": None}

    # ===================================================================
    # AUTONOMOUS SELF-IMPROVEMENT ENGINE
    # ===================================================================
    print("🧠 Running Runtime Intelligence Analyzer...")

    analysis_suggestions = analyze_system_performance(runtime_metrics, model_health)

    # === Self-Optimization Engine ===
    if analysis_suggestions:
        optimized = apply_self_optimization(self_improvement_log, model_health)
        if optimized:
            # บันทึก model_health ใหม่
            health_path = MEMORY / "model_health.json"
            save_json(health_path, model_health)
            print("🔄 ระบบได้ปรับน้ำหนักโมเดลอัตโนมัติแล้ว")

    # บันทึกผลการวิเคราะห์
    if analysis_suggestions:
        if "suggestions" not in self_improvement_log:
            self_improvement_log["suggestions"] = []
        
        self_improvement_log["suggestions"].extend(analysis_suggestions)
        self_improvement_log["last_analysis"] = dt.datetime.now().isoformat()

        print(f"📊 AI Self-Analysis: พบ {len(analysis_suggestions)} ข้อเสนอแนะ")

        # แสดงสรุปข้อเสนอแนะสำคัญ
        high_priority = [s for s in analysis_suggestions if s.get("priority") == "high"]
        if high_priority:
            print("🚨 High Priority Suggestions:")
            for s in high_priority[:3]:
                print(f"   • {s['issue']}")
                print(f"     → {s['suggestion']}")
    else:
        print("✅ No critical issues found.")

    # === ส่วนเดิมของ update_memory (Challenger Queue, Decisions, etc.) ===
    all_models = candidates["coding_analysis"] + candidates["research_reasoning"]
    registry["models"].extend(all_models)

    run_id = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    history["runs"].append({
        "run_id": run_id,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "report_path": str(report_path.relative_to(ROOT)),
        "recommendations": recommendations
    })

    # === Challenger Queue Logic ===
    for category, models in candidates.items():
        if not models:
            continue

        best_model = max(models, key=lambda m: m.get("total_score", 0))
        current_champion = champion_models["champions"].get(category)

        challenger_path = MEMORY / "challenger_queue.json"
        challenger_memory = load_json(challenger_path)

        if "challengers" not in challenger_memory:
            challenger_memory["challengers"] = []

        current_model_name = current_champion.get("model_name") if current_champion else "None"

        challenger_memory["challengers"].append({
            "timestamp": dt.datetime.now().isoformat(),
            "run_id": run_id,
            "category": category,
            "current_model": current_model_name,
            "current_score": current_champion.get("total_score", 0) if current_champion else 0,
            "challenger_model": best_model.get("name"),
            "challenger_model_id": best_model.get("model_id"),
            "challenger_score": best_model.get("total_score", 0),
            "improvement": best_model.get("total_score", 0) - (current_champion.get("total_score", 0) if current_champion else 0),
            "benchmark_score": best_model.get("benchmark_score", 0)
        })

        save_json(challenger_path, challenger_memory)

        # อัพเดท Champion
        if (current_champion is None or 
            best_model.get("total_score", 0) > current_champion.get("total_score", 0)):
            champion_models["champions"][category] = {
                "run_id": run_id,
                "created_at": dt.datetime.now().isoformat(timespec="seconds"),
                "category": category,
                "model_name": best_model.get("name"),
                "model_id": best_model.get("model_id"),
                "provider": best_model.get("provider"),
                "benchmark_score": best_model.get("benchmark_score"),
                "total_score": best_model.get("total_score"),
                "status": "champion_candidate_pending_human_approval"
            }

    # === Decisions Logic (ส่วนเดิม) ===
    decisions = []
    for category, champion in champion_models["champions"].items():
        if not champion:
            continue
        benchmark_score = champion.get("benchmark_score", 0)
        total_score = champion.get("total_score", 0)

        decision = "KEEP_CURRENT"
        if benchmark_score >= 8 and total_score >= 90:
            decision = "REPLACE_AFTER_APPROVAL"
        elif benchmark_score >= 5 and total_score >= 80:
            decision = "TEST_FIRST"
        elif benchmark_score <= 2:
            decision = "REJECT"

        decision_record = {
            "run_id": run_id,
            "created_at": dt.datetime.now().isoformat(timespec="seconds"),
            "category": category,
            "model_name": champion.get("model_name"),
            "model_id": champion.get("model_id"),
            "decision": decision,
            "benchmark_score": benchmark_score,
            "total_score": total_score
        }
        decisions.append(decision_record)

    decision_history["decisions"].extend(decisions)

    # === Improvement Items ===
    improvement_items = []
    for category, models in candidates.items():
        for model in models:
            benchmark_score = model.get("benchmark_score", 0)
            benchmark = model.get("benchmark", {})

            if benchmark_score <= 3:
                improvement_items.append({
                    "run_id": run_id,
                    "created_at": dt.datetime.now().isoformat(timespec="seconds"),
                    "category": category,
                    "model_name": model.get("name"),
                    "model_id": model.get("model_id"),
                    "issue": "Low benchmark score",
                    "suggested_improvement": "Improve benchmark prompt or reject weak model.",
                    "benchmark_score": benchmark_score,
                    "error": benchmark.get("error")
                })

    self_improvement_log["improvements"].extend(improvement_items)

    # === บันทึกไฟล์ทั้งหมด ===
    save_json(benchmark_path, benchmark_history)
    save_json(agent_review_path, agent_review_history)
    save_json(champion_path, champion_models)
    save_json(decision_path, decision_history)
    save_json(self_improvement_path, self_improvement_log)
    save_json(runtime_metrics_path, runtime_metrics)

    print("Memory updated successfully with Self-Improvement Analysis.")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run without external APIs"
    )

    parser.add_argument(
        "--api",
        choices=["openrouter"],
        help="Use live API mode"
    )

    args = parser.parse_args()

    if not args.mock and not args.api:
        print("Please run with --mock first.")
        print("Example: python 04_scripts/run_orchestrator.py --mock")
        return

    current_stack = load_json(
        MEMORY / "current_stack.json"
    )

    runtime_config = load_json(
        MEMORY / "agent_runtime_config.json"
    )

    runtime_metrics_path = MEMORY / "runtime_metrics.json"

    if runtime_metrics_path.exists():
        runtime_metrics = load_json(runtime_metrics_path)
    else:
        runtime_metrics = {
            "runs": []
        }

    runtime_metrics_path = (
        MEMORY / "runtime_metrics.json"
    )

    runtime_metrics = load_json(
        runtime_metrics_path
    )

    agent_team_review = None

     # เลือกโมเดลตาม task complexity
    coding_model = choose_model_for_task(
        "coding_agent",
        task_prompt="Write a simple Python function...",  # สามารถใส่ตัวอย่างได้
        task_complexity="cheap"
    )

    research_model = choose_model_for_task(
        "research_agent",
        task_prompt="Compare open-source AI models...", 
        task_complexity="reasoning"
    )

    orchestrator_model = choose_model_for_task(
        "orchestrator",
        task_complexity="normal"
    )

    if args.api == "openrouter":

        if not os.getenv("OPENROUTER_API_KEY"):
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set."
            )

        print("Using OpenRouter live API mode...")

        candidates = fetch_openrouter_models()
        candidates = benchmark_models(candidates)

        agent_team_review = run_agent_team_review(
            candidates,
            runtime_config,
            runtime_metrics,
            runtime_metrics_path
        )

    else:

        candidates = mock_candidates()

    recommendations = compare_to_current(
        current_stack,
        candidates
    )

    # โหลด self_improvement_log เพื่อส่งให้ report
    self_improvement_path = MEMORY / "self_improvement_log.json"
    if self_improvement_path.exists():
        self_improvement_log = load_json(self_improvement_path)
    else:
        self_improvement_log = {"improvements": [], "suggestions": [], "last_analysis": None}

    report_path = write_report(
        candidates,
        recommendations,
        agent_team_review,
        self_improvement_log   # ← ส่งตัวแปรที่โหลดแล้ว
    )

    update_memory(
    candidates,
    recommendations,
    report_path,
    runtime_metrics,        # ← เพิ่ม
    runtime_metrics_path,   # ← เพิ่ม
    agent_team_review
)

    print("MVP run completed.")
    print(f"Report created: {report_path}")
    print(
        "Check 00_memory/approval_queue.json for human approval requests."
    )


if __name__ == "__main__":
    main()

