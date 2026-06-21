# =====================================================================
# 🚀 BASE44 ENGINE V7.1.0: REAL-TIME SERPER SEARCH INTEGRATION
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V7.1.0")

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root_handler(): return Response(content="OK", status_code=200)

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health_check(): return Response(content="OK", status_code=200)

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
            response = await client.post(
                "https://google.serper.dev/search",
                headers={"X-API-KEY": cls.API_KEY, "Content-Type": "application/json"},
                json={"q": query, "num": 5},
                timeout=10.0
            )
            data = response.json()
            results = data.get("organic", [])
            return "\n".join([f"• {r['title']}: {r['link']}" for r in results[:3]])

class PetCareHunter:
    @staticmethod
    async def get_real_deals():
        data = await SearchEngine.search("สินค้า Pet Care ขายดี Shopee Affiliate คอมมิชชั่นสูง")
        return (
            "🐾 [รายงานพิเศษ: Pet Care Hunter (Real-time)]\n\n"
            "🔍 ผลการค้นหาดีลทำเงินในตลาดปัจจุบัน:\n"
            f"{data}\n\n"
            "💡 บอสเลือกจากลิงก์ข้างบน หรือพิมพ์ชื่อแบรนด์มาได้เลยครับ เดี๋ยวผมร่าง Content ให้!"
        )

class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        if "/findpets" in text_lower:
            await Messenger.send("🐾 [Pet Care Hunter กำลังสแกนดีลจริง... รอสักครู่ครับ]")
            report = await PetCareHunter.get_real_deals()
            await Messenger.send(report)
        elif any(brand in text_lower for brand in ["petsoft", "odorguard", "furdetangler"]):
            selected_brand = text.strip()
            await Messenger.send(f"📝 [Content Creator]: กำลังร่างเนื้อหาขาย '{selected_brand}'...\n\n(ระบบ Content พร้อมทำงานแล้วครับบอส)")
        elif "report bu.1" in text_lower:
            await Messenger.send("📊 [BU.1 รายงาน]: ระบบพร้อมสแกนดีลจริงผ่าน /findpets ครับ")
        else:
            await Messenger.send("✅ ระบบพร้อมทำงาน:\n- /findpets [สแกนสินค้าสัตว์เลี้ยง]\n- report bu.1")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

scheduler = AsyncIOScheduler(timezone=timezone('Asia/Bangkok'))
scheduler.add_job(lambda: asyncio.create_task(Messenger.send("☀️ อรุณสวัสดิ์ครับบอส! ระบบรายงานยุทธศาสตร์พร้อมวิเคราะห์โอกาสทำเงินวันนี้ครับ")), 'cron', hour=9, minute=0)
scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))