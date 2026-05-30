import os
import asyncio
import logging
from pathlib import Path
import sys

# ป้องกันปัญหาเรื่อง Path เวลาเรียกใช้ข้ามโฟลเดอร์บนเซิร์ฟเวอร์ Render
sys.path.append(str(Path(__file__).resolve().parents[1] / "04_scripts"))

# เปลี่ยนมาใช้ httpx เพื่อประสิทธิภาพ Async สูงสุดตามมาตรฐานปี 2026
import httpx

logger = logging.getLogger(__name__)

class ProviderRouter:
    def __init__(self):
        # โหลด API Keys จาก Environment Variables (.env หรือจากระบบ Render)
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        
        # รหัส HTTP Error Codes ที่แปลว่าระบบล่ม/จำกัดสิทธิ์ เพื่อสั่งสลับ Provider ทันที
        self.failover_errors = [429, 402, 403, 500, 502, 503, 504]

    async def _call_groq(self, prompt: str, model: str = "llama3-8b-8192") -> str:
        """ยิงแบบ Async ตรงเข้า Groq API (เน้นความเร็วสูงและฟรี)"""
        if not self.groq_key:
            raise ValueError("Missing GROQ_API_KEY")
            
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            response.raise_for_status()

    async def _call_gemini(self, prompt: str, model: str = "gemini-1.5-flash") -> str:
        """ยิงแบบ Async ตรงเข้า Google AI Studio (Free-tier โควตาสูง)"""
        if not self.gemini_key:
            raise ValueError("Missing GEMINI_API_KEY")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.gemini_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json" # บังคับให้ Gemini คืนค่าเป็น JSON เสมอเพื่อเอาไปใช้ใน Router ปลอดภัย 100%
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=12.0)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            response.raise_for_status()

    async def _call_openrouter(self, prompt: str, model: str = "google/gemini-2.5-flash:free") -> str:
        """ยิงแบบ Async เข้า OpenRouter (ตัวสำรองโมเดลฟรีสารพัดประโยชน์)"""
        if not self.openrouter_key:
            raise ValueError("Missing OPENROUTER_API_KEY")
            
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=15.0)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            response.raise_for_status()

    async def request_llm(self, prompt: str, tier: str = "fast") -> str:
        """
        ฟังก์ชันหลักที่เป็นโล่กำบังระบบ (Smart Routing + Failover Engine)
        """
        # กำหนดเส้นทางการสลับค่ายอัตโนมัติ (Fallback Chains)
        if tier == "reasoning":
            chain = [
                {"name": "Gemini (Main-Reasoning)", "func": lambda: self._call_gemini(prompt)},
                {"name": "OpenRouter-Gemini (Backup-Reasoning)", "func": lambda: self._call_openrouter(prompt, "google/gemini-2.5-flash:free")}
            ]
        else: # tier == "fast"
            chain = [
                {"name": "Groq (Main-Fast)", "func": lambda: self._call_groq(prompt)},
                {"name": "OpenRouter-Llama (Backup-Fast)", "func": lambda: self._call_openrouter(prompt, "meta-llama/llama-3-8b-instruct:free")},
                {"name": "Gemini-Backup", "func": lambda: self._call_gemini(prompt)}
            ]

        # วนลูปสลับค่ายอัตโนมัติเมื่อเจอปัญหา
        for provider in chain:
            try:
                logger.info(f"🔌 [LLM Router] Connecting to: {provider['name']}")
                result = await provider["func"]()
                if result and result.strip():
                    logger.info(f"✅ [LLM Router] Success via: {provider['name']}")
                    return result
            except httpx.TimeoutException:
                logger.warning(f"⚠️ [Failover Trigger] {provider['name']} TIMEOUT! สลับไปค่ายถัดไป...")
                continue
            except httpx.HTTPStatusError as e:
                status_code = e.response.status_code
                if status_code in self.failover_errors:
                    logger.warning(f"⚠️ [Failover Trigger] {provider['name']} ติดปัญหาโค้ด {status_code} (Rate Limit/Quota Full) สลับไปค่ายถัดไป...")
                    continue
                else:
                    logger.error(f"❌ HTTP Error ใน {provider['name']}: {e}")
                    continue
            except Exception as e:
                logger.error(f"❌ Unknown Error ใน {provider['name']}: {e}")
                continue
                
        # หากทุกค่ายโควตาฟรีหมดพร้อมกันในวันนั้น จะส่ง Error ไปบอกเพื่อให้ระบบใช้ Static Fallback Rule ใน meta_orchestrator
        raise RuntimeError("🚨 โควตา API ฟรีเต็มหมดทุกค่ายแล้วสำหรับวันนี้!")

# สร้าง Instance พร้อมใช้งานข้ามโมดูล
provider_router = ProviderRouter()