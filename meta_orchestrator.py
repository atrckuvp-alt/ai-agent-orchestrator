# =====================================================================
# 🚀 BU.1 ENGINE V15.0.0: FULL PROACTIVE & ANALYTIC PRODUCTION SYSTEM
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="BU.1 Expert System")

# --- Route สำหรับ Render เพื่อป้องกัน 404 ---
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
        data = await SearchEngine.search(f"รีวิวความน่าเชื่อถือ {brand} ผู้ใช้จริง แบรนด์ยั่งยืน")
        return f"🔎 [ดร.แสงสุข - Consumer Insight & Sustainability]:\n{data}"
    
    @staticmethod
    async def khun_anish_analysis(brand):
        data = await SearchEngine.search(f"วิเคราะห์ Market Gap และ Hidden Pain Points ของ {brand}")
        return f"🧠 [คุณอนิศ - Strategic Analysis & Leverage]:\n{data}"
    
    @staticmethod
    async def khun_sittinan_growth(brand):
        data = await SearchEngine.search(f"เทรนด์การค้นหา สถิติยอดขาย Conversion Rate ของ {brand}")
        return f"📊 [คุณสิทธินันท์ - Growth Marketing Analytics]:\n{data}"

class BU1_Orchestrator:
    async def execute_bu1_cycle(self, product):
        credibility = await ExpertAgents.dr_sangsook_filter(product)
        analysis = await ExpertAgents.khun_anish_analysis(product)
        content = await ExpertAgents.khun_sittinan_growth(product)
        return f"{credibility}\n\n{analysis}\n\n{content}\n\n✅ [สรุปจาก BU.1]: ข้อมูลเชิงลึกสแกนเรียบร้อยครับบอส!"

class ProactiveSourcing:
    @staticmethod
    async def get_blue_ocean_deals():
        deals = await SearchEngine.search("สินค้า Pet Care ขายดี Blue Ocean Affiliate 2026")
        samples = await SearchEngine.search("สินค้าสัตว์เลี้ยง แจกฟรี ทดลองใช้ 2026")
        return (
            "🏢 [คุณศุภจี]: รายงานสรรหาสินค้าจากทีม BU.1 ครับ:\n\n"
            "🌊 [Blue Ocean Opportunities]:\n" + deals + "\n\n"
            "🎁 [Free Sample Alert]:\n" + samples + "\n\n"
            "👉 บอสเลือกตัวที่ชอบแล้วพิมพ์ 'analyze [ชื่อสินค้า]' ให้ทีมงานเจาะลึกได้เลยครับ!"
        )

class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        if "/findpets" in text_lower:
            await Messenger.send("🏢 [คุณศุภจี]: รับทราบ! สั่งทีม BU.1 สแกนหาขุมทรัพย์ด่วนครับ...")
            report = await ProactiveSourcing.get_blue_ocean_deals()
            await Messenger.send(report)
        elif text_lower.startswith("analyze"):
            brand = text.replace("analyze", "").strip()
            if not brand: brand = "สินค้าทั่วไป"
            await Messenger.send(f"🏢 [คุณศุภจี]: รับทราบ! จ่ายงานให้ทีม BU.1 เจาะลึกข้อมูลจริงของ {brand} ครับ")
            report = await BU1_Orchestrator().execute_bu1_cycle(brand)
            await Messenger.send(report)
        else:
            await Messenger.send("✅ ระบบพร้อม:\n- /findpets [สแกนหาของดี]\n- analyze [ชื่อสินค้า] [เจาะลึก]")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))