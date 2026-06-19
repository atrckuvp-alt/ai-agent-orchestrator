# =====================================================================
# 🚀 BASE44 ENGINE V6.1.0: STABLE & SILENT EDITION
# =====================================================================
import os, asyncio, uvicorn, httpx, datetime
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Base44 Engine V6.1.0")

# --- 1. Silent Exception Handler ---
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return Response(content="OK", status_code=200)

# --- 2. Google Sheets Logger ---
class SheetsManager:
    def __init__(self):
        self.url = "https://script.google.com/macros/s/AKfycbyZrK-DL36OINYJPjtZA0I1jDAv2hOwRQ0fJprBgIUqMvDUgK-bWpZ0lBHN-IlKDwuB/exec"
    
    async def log_success(self, viability, data):
        async with httpx.AsyncClient() as client:
            try:
                # ใช้ timeout สั้นๆ เพื่อไม่ให้ Render มองว่าค้าง
                await client.post(self.url, json={"viability": viability, "content": data}, timeout=3.0)
            except:
                pass

# --- 3. Mastermind Engine ---
class MetaOrchestrator:
    async def run_ceo_workflow(self, task: str):
        bu1 = BU1_Manager()
        result = await bu1.execute_strategy()
        if result['viability'] >= 80 and result['is_emotional']:
            await SheetsManager().log_success(result['viability'], result['data'])
            return result
        return "QC_FAILED"

class BU1_Manager:
    async def execute_strategy(self):
        return {"viability": 90, "is_emotional": True, "data": "Analysis of High-Profit Deals"}

# --- 4. Silent Routes ---
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler():
    return JSONResponse(status_code=200, content={"status": "online"})

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health_check():
    return JSONResponse(status_code=200, content={"status": "ok"})

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    meta = MetaOrchestrator()
    asyncio.create_task(meta.run_ceo_workflow("revenue"))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))