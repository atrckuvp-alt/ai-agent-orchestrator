# =====================================================================
# 🚀 BASE44 ENGINE V6.2.0: COMMAND CENTER EDITION
# =====================================================================
import os, asyncio, uvicorn, httpx, datetime
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Base44 Engine V6.2.0")

# --- 1. Command Center (Search & Summarize) ---
class CommandCenter:
    async def process_command(self, text: str):
        if text.startswith("/search"):
            query = text.replace("/search", "").strip()
            return f"🔍 กำลังค้นหายุทธศาสตร์เรื่อง: {query}... (กำลังพัฒนาระบบ Search API)"
        elif text.startswith("/summarize"):
            topic = text.replace("/summarize", "").strip()
            return f"📝 กำลังสรุปข้อมูลเชิงลึกเรื่อง: {topic}... (กำลังประมวลผล Mastermind)"
        return None

# --- 2. Google Sheets Logger ---
class SheetsManager:
    def __init__(self):
        self.url = "https://script.google.com/macros/s/AKfycbyZrK-DL36OINYJPjtZA0I1jDAv2hOwRQ0fJprBgIUqMvDUgK-bWpZ0lBHN-IlKDwuB/exec"
    
    async def log_success(self, viability, data):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.url, json={"viability": viability, "content": data}, timeout=3.0)
            except: pass

# --- 3. Mastermind & Webhook ---
class MetaOrchestrator:
    async def run_ceo_workflow(self, task: str):
        # ตรวจสอบก่อนว่าเป็น Command พิเศษไหม
        cmd_center = CommandCenter()
        cmd_result = await cmd_center.process_command(task)
        if cmd_result:
            return {"viability": 100, "is_emotional": True, "data": cmd_result}
            
        # ถ้าไม่ใช่ Command ให้รันงานปกติ
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
    # ดึงข้อความจาก Telegram
    text = data.get("message", {}).get("text", "")
    meta = MetaOrchestrator()
    asyncio.create_task(meta.run_ceo_workflow(text))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))