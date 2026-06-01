import json
import os
import datetime as dt
from pathlib import Path
import base64
from provider_router import provider_router

ROOT = Path(__file__).resolve().parents[1]
MEMORY_DIR = ROOT / "00_memory" / "user_memories"

class MemoryManager:
    def __init__(self):
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        # ดึงสิทธิ์ GitHub เพื่อใช้เป็นหน่วยความจำถาวรฟรี 100% กรณี Render รีสตาร์ทตัวเอง
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPOSITORY")  # รูปแบบ "username/repo"

    def _get_user_path(self, user_id: int) -> Path:
        return MEMORY_DIR / f"{user_id}.json"

    def load_memory(self, user_id: int) -> dict:
        path = self._get_user_path(user_id)
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "user_id": user_id,
            "short_term_buffer": [],
            "long_term_summary": {
                "last_updated": "",
                "business_context": "ไม่มีบริบทก่อนหน้านี้",
                "teams_discovered": [],
                "workflows_used": [],
                "discovered_open_source": [],
                "cost_optimization_logs": [],
                "essential_keywords": []
            }
        }

    def save_memory(self, user_id: int, memory_data: dict):
        path = self._get_user_path(user_id)
        json_content = json.dumps(memory_data, indent=2, ensure_ascii=False)
        path.write_text(json_content, encoding="utf-8")

        # สั่งอัปโหลดขึ้น GitHub ทันทีเพื่อความคงทนถาวร (ถ้ามีการคอนฟิก TOKEN ไว้ใน Render ENV)
        if self.github_token and self.github_repo:
            try:
                import httpx
                import asyncio
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_running():
                        loop.create_task(self._sync_to_github(user_id, json_content))
                except RuntimeError:
                    asyncio.run(self._sync_to_github(user_id, json_content))
            except Exception as e:
                print(f"⚠️ [GitHub Sync Warning] ล้มเหลว: {e}")

    async def _sync_to_github(self, user_id: int, content: str):
        import httpx
        path_in_repo = f"00_memory/user_memories/{user_id}.json"
        url = f"https://api.github.com/repos/{self.github_repo}/contents/{path_in_repo}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with httpx.AsyncClient() as client:
            sha = None
            res = await client.get(url, headers=headers)
            if res.status_code == 200:
                sha = res.json().get("sha")
            payload = {
                "message": f"🧠 AI-BOS Memory System Event Loop: Update User {user_id}",
                "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
            }
            if sha:
                payload["sha"] = sha
            await client.put(url, json=payload, headers=headers)

    def add_to_short_term(self, user_id: int, role: str, content: str):
        memory = self.load_memory(user_id)
        memory["short_term_buffer"].append({"role": role, "content": content})
        # สไลด์คุมประวัติบทสนทนาดิบไว้ไม่เกิน 3 ชุดล่าสุดเพื่อป้องกัน RAM 512MB เต็ม
        if len(memory["short_term_buffer"]) > 3:
            memory["short_term_buffer"] = memory["short_term_buffer"][-3:]
        self.save_memory(user_id, memory)

    async def compress_and_update_long_term(self, user_id: int):
        memory = self.load_memory(user_id)
        if not memory["short_term_buffer"]:
            return

        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in memory["short_term_buffer"]])
        current_summary = json.dumps(memory["long_term_summary"], ensure_ascii=False)

        prompt = f"""
        คุณคือ 'ตัวสกัดประสบการณ์สะสมระยะยาว' ของระบบ AI Business Operating System (AI-BOS)
        จงอ่านบทสนทนาล่าสุดแล้วประมวลผลควบรวมเข้ากับข้อมูลหน่วยความจำเดิม สกัดเฉพาะคีย์เวิร์ด เอนทิตีเทคนิค และบริบทเชิงธุรกิจอย่างกระชับ ห้ามบันทึกคำพูดลอยๆ

        ความจำระยะยาวเดิม:
        {current_summary}

        บทสนทนาล่าสุด:
        {history_text}

        จงตอบกลับด้วยรูปแบบ JSON นี้เท่านั้น ห้ามมีข้อความอื่นปนเด็ดขาด:
        {{
            "business_context": "บริบทเป้าหมายสูงสุดของบริษัทผู้ใช้งานในปัจจุบัน",
            "teams_discovered": ["อาร์เรย์รายชื่อทีมที่เคยสร้างหรือเรียกใช้งาน ห้ามซ้ำกับของเดิม"],
            "workflows_used": ["อาร์เรย์สรุปเวิร์กโฟลว์ทางเทคนิคที่เคยใช้ เช่น weekly_ai_model_research_mvp_v1"],
            "discovered_open_source": ["ซอฟต์แวร์โอเพนซอร์สหรือโมเดลฟรีที่ค้นพบและนำมาประยุกต์ใช้"],
            "cost_optimization_logs": ["รายการคำแนะนำเกี่ยวกับการจัดคอสหรือประหยัดทรัพยากรที่เคยเสนอสำเร็จ"],
            "essential_keywords": ["คีย์เวิร์ดดัชนีสั้นๆ รวมเรื่องทั้งหมดจำกัดไม่เกิน 15 คำ"]
        }}
        """
        try:
            ai_response = await provider_router.request_llm(prompt, tier="fast")
            cleaned_json = ai_response.replace("```json", "").replace("```", "").strip()
            new_summary = json.loads(cleaned_json)
            new_summary["last_updated"] = dt.datetime.now().isoformat()
            memory["long_term_summary"] = new_summary
            self.save_memory(user_id, memory)
        except Exception as e:
            print(f"⚠️ [Memory Management Engine Error]: {e}")

memory_manager = MemoryManager()