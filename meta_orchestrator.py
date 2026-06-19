# =====================================================================
# 🚀 BASE44 ENGINE V6.3.0: FULL SERPER.DEV INTEGRATION
# =====================================================================
import os, asyncio, uvicorn, httpx, datetime
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Base44 Engine V6.3.0")

# --- 1. Search Engine (Serper.dev) ---
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

# --- 2. Google Sheets Logger ---
class SheetsManager:
    def __init__(self):
        self.url = "https://script.google.com/macros/s/AKfycbyZrK-DL36OINYJPjtZA0I1jDAv2hOwRQ0fJprBgIUqMvDUgK-bWpZ0lBHN-IlKDwuB/exec"
    
    async def log_success(self, viability, data):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.url, json={"viability": viability, "content": data}, timeout=3.0)
            except: pass

# --- 3. Mastermind & Command Center ---
class CommandCenter:
    async def process_command(self, text: str):
        if text.startswith("/search"):
            query = text.replace("/search", "").strip()
            search = SearchEngine()
            results = await search.search(query)
            return f"🔍 ผลการค้นหาสำหรับ '{query}':\n\n{results}"
        return None

class MetaOrchestrator:
    async def run_ceo_workflow(self, text: str):
        # 1. เช็ค Command ก่อน
        cmd_result = await CommandCenter().process_command(text)
        if cmd_result:
            return {"viability": 100, "is_emotional": True, "data": cmd_result}
            
        # 2. ถ้าไม่ใช่ Command ให้รันระบบบริหารปกติ
        bu1 = BU1_Manager()
        result = await bu1.execute_strategy()
        if result['viability'] >= 80:
            await SheetsManager().log_success(result['viability'], result['data'])
            return result
        return "QC_FAILED"

class BU1_Manager:
    async def execute_strategy(self):
        return {"viability": 90, "is_emotional": True, "data": "Analysis of High-Profit Deals"}

# --- 4. Routes ---
@app.exception_handler(404)
async def custom_404_handler(_, __): return Response(content="OK", status_code=200)

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    meta = MetaOrchestrator()
    # ดึงงานเข้าคิวรันแบบ Async
    asyncio.create_task(meta.run_ceo_workflow(text))
    return Response(content="OK", status_code=200)

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler(): return JSONResponse(status_code=200, content={"status": "online"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))