import os, asyncio, uvicorn, httpx
import google.generativeai as genai
from fastapi import FastAPI, Request, Response

app = FastAPI()

# 1. Health Check (แก้ 404/405)
@app.api_route("/", methods=["GET", "HEAD", "POST"])
@app.api_route("/health", methods=["GET", "HEAD", "POST"])
async def health_check():
    return Response(status_code=200, content="OK")

# 2. ระบบจัดการ Skill Logic (Multi-Provider Failover)
class AIProvider:
    @staticmethod
    async def call(prompt):
        providers = [
            {"name": "Gemini", "func": AIProvider.call_gemini},
            {"name": "Groq", "func": AIProvider.call_groq},
            {"name": "OpenRouter", "func": AIProvider.call_openrouter}
        ]
        for p in providers:
            try:
                return await p["func"](prompt)
            except Exception as e:
                print(f"Provider {p['name']} error: {str(e)[:50]}")
        return "ระบบประมวลผลติดปัญหา กรุณาลองใหม่อีกครั้ง"

    @staticmethod
    async def call_gemini(prompt):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash')
        return (await asyncio.to_thread(model.generate_content, prompt)).text

    @staticmethod
    async def call_groq(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

    @staticmethod
    async def call_openrouter(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
                json={"model": "meta-llama/llama-3.1-70b-instruct", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

# 3. BU.1 Orchestrator (ดึง Skill ของ ดร.แสงสุข และ คุณสิทธินันท์ มาประมวลผล)
class BU1_Orchestrator:
    async def run_bu1_pipeline(self, query):
        # ดึงข้อมูลตลาดจริง
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        payload = {"q": f"best affiliate products for {query}", "num": 10}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            results = resp.json().get("organic", [])
            market_data = "\n".join([f"- {r.get('title')}" for r in results])
        
        # ใส่ Skill Logic ลงใน Prompt (Hard-coded requirement, no role-play)
        prompt = f"""
        วิเคราะห์ข้อมูลตลาดนี้: {market_data}
        
        ให้ประมวลผลตาม Skill ของทีม BU.1 ดังนี้:
        1. (ดร.แสงสุข - Credibility Filter): คัดกรองสินค้าที่มีความยั่งยืน ไม่ใช่เทรนด์ฉาบฉวย เลือกมา 3 รายการ
        2. (คุณสิทธินันท์ - Viability Score): ระบุเหตุผลว่าทำไมสินค้าทั้ง 3 นี้ถึงทำเงินได้จริง
        3. (สืบหาของฟรี): ค้นหาของฟรี 1 รายการเพื่อใช้ดึง Traffic เข้า Page
        
        ตอบในรูปแบบ Template นี้เท่านั้น:
        ✅ **รายการสินค้าคัดเลือก:**
        1. [ชื่อสินค้า]: [เหตุผลความยั่งยืน]
        2. [ชื่อสินค้า]: [เหตุผลความยั่งยืน]
        3. [ชื่อสินค้า]: [เหตุผลความยั่งยืน]
        
        🎁 **ของฟรีดึง Traffic:**
        - [ชื่อของฟรี]: [เหตุผล]
        
        👉 *พิมพ์ชื่อสินค้าที่บอสเลือก เพื่อให้คุณอนิศเริ่มเขียนคอนเทนต์ปิดการขาย*
        """
        return await AIProvider.call(prompt)

# 4. MetaOrchestrator (CEO คุณศุภจี)
class MetaOrchestrator:
    async def process(self, text):
        try:
            msg = text.strip()
            if "analyze" in msg.lower():
                await self.send_telegram("🏢 [CEO คุณศุภจี]: รับทราบคำสั่ง... กำลังให้ ดร.แสงสุข และ คุณสิทธินันท์ ประมวลผลข้อมูลตลาดครับ")
                res = await BU1_Orchestrator().run_bu1_pipeline(msg.replace("analyze", "").strip())
                await self.send_telegram(f"{res}")
            else:
                await self.send_telegram(f"✍️ [คุณอนิศ]: รับทราบ! กำลังวิเคราะห์ Pain Points และปั้นคอนเทนต์ขาย {msg} ให้ได้ผลลัพธ์สูงสุดครับ...")
                content = await AIProvider.call(f"เขียนคอนเทนต์ Affiliate ขาย {msg} เน้น Market Gap และ Hidden Pain Points เพื่อปิดการขาย")
                await self.send_telegram(f"🚀 [คอนเทนต์จากคุณอนิศ]:\n\n{content}")
        except Exception as e:
            await self.send_telegram(f"❌ [SYSTEM ERROR]: {str(e)}")

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}