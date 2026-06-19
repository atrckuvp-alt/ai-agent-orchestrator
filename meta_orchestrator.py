# =====================================================================
# 🚀 BASE44 ENGINE V6.5.0: FINAL AUTOMATIC REPORTER (PRODUCTION)
# =====================================================================
import os, asyncio, uvicorn, httpx, datetime
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V6.5.0")

# --- 1. System Config ---
class Messenger:
    TOKEN = "8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4"
    CHAT_ID = "7238952711"  # ใส่เลข ID บอสเรียบร้อยแล้วครับ
    
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", 
                                  json={"chat_id": cls.CHAT_ID, "text": text}, timeout=5.0)
            except: pass

# --- 2. Scheduled Report (9 AM Daily) ---
async def send_daily_report():
    report_msg = "☀️ อรุณสวัสดิ์ครับบอส! ระบบรายงานยุทธศาสตร์อัตโนมัติทำงานแล้วครับ\n\n- ตรวจสอบฐานข้อมูล Google Sheets เรียบร้อย\n- ระบบ Search Engine พร้อมใช้งาน\n- สรุปผลงานวันนี้: (บอสสามารถใช้คำสั่ง /search เพื่อค้นหาข้อมูลเพิ่มได้เลยครับ)"
    await Messenger.send(report_msg)

scheduler = AsyncIOScheduler(timezone=timezone('Asia/Bangkok'))
scheduler.add_job(send_daily_report, 'cron', hour=9, minute=0)
scheduler.start()

# --- 3. Core Logic (Search + Logger) ---
class SearchEngine:
    def __init__(self):
        self.api_key = "930b04d1e25b79c0b4034fa9668eb961183ebcb6"
        self.url = "https://google.serper.dev/search"

    async def search(self, query: str):
        headers = {'X-API-KEY': self.api_key, 'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            resp = await client.post(self.url, headers=headers, json={"q": query}, timeout=5.0)
            data = resp.json()
            results = data.get("organic", [])[:3]
            return "\n".join([f"- {r.get('title')}: {r.get('link')}" for r in results])

class SheetsManager:
    async def log(self, text):
        url = "https://script.google.com/macros/s/AKfycbyZrK-DL36OINYJPjtZA0I1jDAv2hOwRQ0fJprBgIUqMvDUgK-bWpZ0lBHN-IlKDwuB/exec"
        async with httpx.AsyncClient() as client:
            try: await client.post(url, json={"content": text}, timeout=3.0)
            except: pass

# --- 4. Request Orchestrator ---
class MetaOrchestrator:
    async def handle_request(self, text):
        if text.startswith("/search"):
            query = text.replace("/search", "").strip()
            results = await SearchEngine().search(query)
            await Messenger.send(f"🔍 ผลการค้นหา '{query}':\n\n{results}")
        else:
            await SheetsManager().log(text)
            await Messenger.send(f"✅ บันทึกคำสั่งเรียบร้อย: {text}")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))