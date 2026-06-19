# =====================================================================
# 🚀 BASE44 ENGINE V6.4.0: FINAL MASTERMIND + TELEGRAM INTEGRATED
# =====================================================================
import os, asyncio, uvicorn, httpx, datetime
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Base44 Engine V6.4.0")

# --- 1. Telegram Messenger (ระบบตอบกลับ) ---
class TelegramMessenger:
    def __init__(self):
        # 🔑 ใส่ TOKEN ที่บอสให้มาเรียบร้อยครับ
        self.token = "8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4"
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    async def send_message(self, chat_id, text):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.url, json={"chat_id": chat_id, "text": text}, timeout=5.0)
            except: pass

# --- 2. Search Engine & Logger ---
class SearchEngine:
    def __init__(self):
        self.api_key = "930b04d1e25b79c0b4034fa9668eb961183ebcb6"
        self.url = "https://google.serper.dev/search"

    async def search(self, query: str):
        headers = {'X-API-KEY': self.api_key, 'Content-Type': 'application/json'}
        payload = {"q": query}
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(self.url, headers=headers, json=payload, timeout=5.0)
                data = resp.json()
                results = data.get("organic", [])[:3]
                return "\n".join([f"- {r.get('title')}: {r.get('link')}" for r in results])
            except:
                return "ไม่สามารถเชื่อมต่อระบบค้นหาได้ในขณะนี้"

class SheetsManager:
    def __init__(self):
        self.url = "https://script.google.com/macros/s/AKfycbyZrK-DL36OINYJPjtZA0I1jDAv2hOwRQ0fJprBgIUqMvDUgK-bWpZ0lBHN-IlKDwuB/exec"
    
    async def log_success(self, viability, data):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.url, json={"viability": viability, "content": data}, timeout=3.0)
            except: pass

# --- 3. Orchestrator ---
class MetaOrchestrator:
    async def handle_request(self, data):
        chat_id = data.get("message", {}).get("chat", {}).get("id")
        text = data.get("message", {}).get("text", "")
        if not chat_id: return
        
        # ค้นหา Command
        if text.startswith("/search"):
            query = text.replace("/search", "").strip()
            results = await SearchEngine().search(query)
            await TelegramMessenger().send_message(chat_id, f"🔍 ผลการค้นหาสำหรับ '{query}':\n\n{results}")
        else:
            # รันงานปกติ
            result = await BU1_Manager().execute_strategy()
            if result['viability'] >= 80:
                await SheetsManager().log_success(result['viability'], result['data'])
                await TelegramMessenger().send_message(chat_id, f"✅ วิเคราะห์เสร็จสิ้น: {result['data']}")

class BU1_Manager:
    async def execute_strategy(self):
        return {"viability": 90, "is_emotional": True, "data": "Analysis of High-Profit Deals"}

# --- 4. Routes ---
@app.exception_handler(404)
async def custom_404_handler(_, __): return Response(content="OK", status_code=200)

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    asyncio.create_task(MetaOrchestrator().handle_request(data))
    return Response(content="OK", status_code=200)

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler(): return JSONResponse(status_code=200, content={"status": "online"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))