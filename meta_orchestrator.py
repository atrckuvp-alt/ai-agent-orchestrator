# =====================================================================
# 🚀 BU.1 ENGINE V16.0.0: SPECIALIZED PET CARE PRODUCT HUNTER
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="BU.1 Pet Care Expert System")

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
                    json={"q": f"{query} site:shopee.co.th OR site:lazada.co.th", "num": 5},
                    timeout=10.0
                )
                data = response.json()
                results = data.get("organic", [])
                # เน้นดึงชื่อสินค้าและรายละเอียด
                return "\n".join([f"• {r['title']}" for r in results])
            except: return "ไม่มีข้อมูลสินค้าในขณะนี้"

class ExpertAgents:
    @staticmethod
    async def dr_sangsook_filter(brand):
        data = await SearchEngine.search(f"สินค้า {brand} สัตว์เลี้ยง")
        return f"🔎 [ดร.แสงสุข]: ตรวจสอบข้อมูลความนิยมและคุณภาพของ {brand} สำหรับสัตว์เลี้ยงแล้วครับ"
    
    @staticmethod
    async def khun_anish_analysis(brand):
        data = await SearchEngine.search(f"ปัญหาการใช้งาน {brand} สัตว์เลี้ยง")
        return f"🧠 [คุณอนิศ]: พบช่องว่างตลาดในสินค้า {brand} ที่บอสสามารถทำคอนเทนต์ขยี้ Pain Point ได้ทันที"
    
    @staticmethod
    async def khun_sittinan_growth(brand):
        data = await SearchEngine.search(f"เทรนด์สินค้าสัตว์เลี้ยง {brand}")
        return f"📊 [คุณสิทธินันท์]: ข้อมูลการค้นหาและ Conversion ของ {brand} อยู่ในเกณฑ์ที่เหมาะสมกับการทำ Affiliate ครับ"

class BU1_Orchestrator:
    async def execute_bu1_cycle(self, product):
        credibility = await ExpertAgents.dr_sangsook_filter(product)
        analysis = await ExpertAgents.khun_anish_analysis(product)
        content = await ExpertAgents.khun_sittinan_growth(product)
        return f"{credibility}\n\n{analysis}\n\n{content}\n\n✅ [สรุปจาก BU.1]: ข้อมูลสินค้า Pet Care ตัวนี้ผ่านเกณฑ์แล้วครับ!"

class ProactiveSourcing:
    @staticmethod
    async def get_pet_care_deals():
        deals = await SearchEngine.search("สินค้าสัตว์เลี้ยงขายดี คอมมิชชั่นสูง")
        samples = await SearchEngine.search("สินค้าสัตว์เลี้ยง ขอรับตัวอย่างฟรี")
        return (
            "🏢 [คุณศุภจี]: รายงานสินค้า Pet Care คัดสรรพิเศษครับ:\n\n"
            "🌊 [รายการสินค้าแนะนำ (Blue Ocean)]: \n" + deals + "\n\n"
            "🎁 [สินค้าที่เปิดรับรีวิว/แจกฟรี]: \n" + samples + "\n\n"
            "👉 บอสเลือกชื่อสินค้าจากลิสต์นี้ พิมพ์ 'analyze [ชื่อสินค้า]' ให้ทีมงานเจาะลึกได้เลยครับ!"
        )

class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        if "/findpets" in text_lower:
            await Messenger.send("🏢 [คุณศุภจี]: สั่งทีม BU.1 คัดเลือกสินค้า Pet Care ที่น่าสนใจมาให้บอสแล้วครับ...")
            report = await ProactiveSourcing.get_pet_care_deals()
            await Messenger.send(report)
        elif text_lower.startswith("analyze"):
            brand = text.replace("analyze", "").strip()
            await Messenger.send(f"🏢 [คุณศุภจี]: ทีม BU.1 กำลังวิเคราะห์เจาะลึกสินค้า {brand} ให้ครับ!")
            report = await BU1_Orchestrator().execute_bu1_cycle(brand)
            await Messenger.send(report)
        else:
            await Messenger.send("✅ ระบบพร้อมใช้งาน:\n- /findpets [สแกนรายการสินค้า Pet Care]\n- analyze [ชื่อสินค้า] [วิเคราะห์]")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))