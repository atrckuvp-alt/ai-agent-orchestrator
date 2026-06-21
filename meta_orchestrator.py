# =====================================================================
# 🚀 BU.1 ENGINE V14.0.0: REAL-DATA INTEGRATED PRODUCTION SYSTEM
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="BU.1 Expert System")

# --- Essential Routes for Render ---
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return Response(content="OK", status_code=200)

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health(): return Response(content="OK", status_code=200)

class Messenger:
    TOKEN = "8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4"
    CHAT_ID = "7238952711"
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text}, timeout=10.0)
            except: pass

class SearchEngine:
    API_KEY = "930b04d1e25b79c0b4034fa9668eb961183ebcb6"
    @classmethod
    async def search(cls, query: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://google.serper.dev/search",
                    headers={"X-API-KEY": cls.API_KEY, "Content-Type": "application/json"},
                    json={"q": query, "num": 3},
                    timeout=10.0
                )
                data = response.json()
                results = data.get("organic", [])
                return "\n".join([f"• {r['title']}: {r.get('snippet', '')}" for r in results])
            except: return "ไม่สามารถดึงข้อมูลได้ในขณะนี้"

class ExpertAgents:
    @staticmethod
    async def dr_sangsook_filter(brand):
        data = await SearchEngine.search(f"รีวิวความน่าเชื่อถือ {brand} ผู้ใช้จริง")
        return f"🔎 [ดร.แสงสุข - Consumer Insight]:\n{data}"
    
    @staticmethod
    async def khun_anish_analysis(brand):
        data = await SearchEngine.search(f"จุดเด่นและปัญหาการใช้งาน {brand}")
        return f"🧠 [คุณอนิศ - Market Gap & Pain Points]:\n{data}"
    
    @staticmethod
    async def khun_sittinan_growth(brand):
        data = await SearchEngine.search(f"เทรนด์การค้นหาและยอดขาย {brand}")
        return f"📊 [คุณสิทธินันท์ - Growth Analytics]:\n{data}"

class BU1_Orchestrator:
    async def execute_bu1_cycle(self, product):
        credibility = await ExpertAgents.dr_sangsook_filter(product)
        analysis = await ExpertAgents.khun_anish_analysis(product)
        content = await ExpertAgents.khun_sittinan_growth(product)
        return f"{credibility}\n\n{analysis}\n\n{content}\n\n✅ [สรุป]: ข้อมูลจริงสแกนเรียบร้อยครับบอส!"

class SupachaiCEO:
    @staticmethod
    def delegate_task(text):
        if "analyze" in text.lower(): return "BU.1"
        return "OTHER"

class MetaOrchestrator:
    async def handle_request(self, text):
        target_bu = SupachaiCEO.delegate_task(text)
        if target_bu == "BU.1":
            brand = text.replace("analyze", "").strip()
            if not brand: brand = "สินค้าทั่วไป"
            await Messenger.send(f"🏢 [คุณศุภจี]: รับทราบครับบอส งานนี้ผมจ่ายให้ทีม BU.1 ดำเนินการวิเคราะห์ข้อมูลจริงด่วน!")
            report = await BU1_Orchestrator().execute_bu1_cycle(brand)
            await Messenger.send(report)
        else:
            await Messenger.send("✅ ระบบพร้อมใช้งาน:\n- พิมพ์ 'analyze [ชื่อสินค้า]' เพื่อส่งงานให้ทีม BU.1 วิเคราะห์เจาะลึกด้วยข้อมูลจริงครับ")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))