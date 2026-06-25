import os, asyncio, uvicorn, httpx
import google.generativeai as genai
from fastapi import FastAPI, Request, Response

app = FastAPI()

# --- 1. ระบบจัดการ Multi-Provider (Failover) ---
class AIProvider:
    @staticmethod
    async def call(prompt):
        # ลำดับการเรียกใช้: Google -> Groq -> OpenRouter -> DeepSeek
        providers = [
            {"name": "Gemini", "func": AIProvider.call_gemini},
            {"name": "Groq", "func": AIProvider.call_groq},
            {"name": "OpenRouter", "func": AIProvider.call_openrouter}
        ]
        for p in providers:
            try:
                return await p["func"](prompt)
            except Exception as e:
                print(f"Provider {p['name']} failed, switching... Error: {e}")
        return "ระบบไม่สามารถประมวลผลได้ในขณะนี้"

    @staticmethod
    async def call_gemini(prompt):
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # ใช้ model ชื่อ 'gemini-1.5-flash' ตามที่ระบบ AI Studio ของบอสรองรับ
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text

    @staticmethod
    async def call_groq(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}"},
                json={"model": "llama3-70b-8192", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

    @staticmethod
    async def call_openrouter(prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}"},
                json={"model": "meta-llama/llama-3-70b-instruct", "messages": [{"role": "user", "content": prompt}]})
            return resp.json()["choices"][0]["message"]["content"]

# --- 2. แก้ไข Route ให้ Render ไม่พ่น 404 ---
@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}