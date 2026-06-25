import os, asyncio, uvicorn, httpx
import google.generativeai as genai
from fastapi import FastAPI, Request, Response

app = FastAPI()

# 1. Health Check (แก้ปัญหา 404/405 ใน Log ของ Render)
@app.api_route("/", methods=["GET", "HEAD", "POST"])
@app.api_route("/health", methods=["GET", "HEAD", "POST"])
async def health_check():
    return Response(status_code=200, content="OK")

# 2. ระบบ Multi-Provider Failover (ครอบคลุมทุกจุด)
async def get_ai_response(prompt):
    providers = [
        {"name": "Gemini", "func": call_gemini},
        {"name": "Groq", "func": call_groq},
        {"name": "OpenRouter", "func": call_openrouter}
    ]
    for p in providers:
        try:
            return await p["func"](prompt)
        except Exception as e:
            print(f"Provider {p['name']} failed, rotating... Error: {e}")
    return "ระบบประมวลผลติดปัญหา กรุณาลองใหม่อีกครั้ง"

async def call_gemini(prompt):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text

async def call_groq(prompt):
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]})
        return resp.json()["choices"][0]["message"]["content"]

async def call_openrouter(prompt):
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
            json={"model": "meta-llama/llama-3.1-70b-instruct", "messages": [{"role": "user", "content": prompt}]})
        return resp.json()["choices"][0]["message"]["content"]

# 3. BU.1 Orchestrator (ดึง Skill ทีมงานมาทำงานจริง)
class BU1_Orchestrator:
    async def run_bu1_pipeline(self, query):
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        payload = {"q": f"best specific product to promote for {query} affiliate", "num": 10}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            results = resp.json().get("organic", [])
            data_points = "\n".join([f"- {r.get('title')}" for r in results])
        
        prompt = f"""
        วิเคราะห์ตลาดสินค้าจากข้อมูล: {data_points}
        
        ประมวลผลโดยใช้ Skill ของทีม BU.1 ดังนี้:
        1. ดร.แสงสุข (Credibility Filter): เลือก 3 สินค้าที่มีความยั่งยืนสูง (ระบุชื่อรุ่น/สินค้าให้ชัดเจน)
        2. คุณสิทธินันท์ (Viability Score): ระบุเหตุผลเชิงกลยุทธ์ว่าทำไมสินค้าทั้ง 3 นี้ถึงทำเงินได้จริง
        3. คุณอนิศ (Freebie Hunter): หาของฟรี 1 รายการในหมวดเดียวกัน เพื่อดึง Traffic
        
        ตอบในรูปแบบ Template นี้เท่านั้น:
        ✅ **รายงานคัดเลือกสินค้าเจาะจง (3 รายการ):**
        1. [ชื่อสินค้า]: [เหตุผลความยั่งยืน & Viability Score]
        2. [ชื่อสินค้า]: [เหตุผลความยั่งยืน & Viability Score]
        3. [ชื่อสินค้า]: [เหตุผลความยั่งยืน & Viability Score]
        
        🎁 **ของฟรีดึง Traffic:**
        - [ชื่อของฟรี]: [เหตุผลที่น่าสนใจ]
        
        👉 *พิมพ์ชื่อสินค้าที่บอสต้องการให้คุณอนิศสร้างคอนเทนต์*
        """
        return await get_ai_response(prompt)

# 4. MetaOrchestrator (CEO)
class MetaOrchestrator:
    async def process(self, text):
        try:
            if "analyze" in text.lower():
                res = await BU1_Orchestrator().run_bu1_pipeline(text.replace("analyze", "").strip())
                await self.send_telegram(f"🏢 [CEO คุณศุภจี]: รายงานสินค้าเจาะจง:\n\n{res}")
            else:
                content = await get_ai_response(f"เขียนคอนเทนต์ขายสินค้า {text} เน้นปิดการขายด้วย Market Gap")
                await self.send_telegram(f"🚀 [คุณอนิศ]: คอนเทนต์พร้อมลุย:\n\n{content}")
        except Exception as e:
            await self.send_telegram(f"❌ [System Error]: {str(e)}")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))