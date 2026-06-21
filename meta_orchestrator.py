# =====================================================================
# 🚀 BASE44 ENGINE V10.1.0: SMART PRODUCT CURATOR
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V10.1.0")

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
            # ปรับให้บอทดึงเฉพาะชื่อสินค้า/หัวข้อที่คัดมาแล้ว
            return "\n".join([f"• {r['title']}" for r in results[:5]])

class AnalyzerAgent:
    @staticmethod
    def run_swot(brand_name: str):
        return (
            f"🧠 [Strategic Analysis: {brand_name}]\n\n"
            "📈 S.W.O.T. Snapshot:\n"
            "• Strength: สินค้ามีจุดขายชัดเจน (High Utility)\n"
            "• Weakness: ตลาดมีการแข่งขันด้านราคาสูง\n"
            "• Opportunity: กลุ่มลูกค้าที่มองหาโซลูชันแก้ปัญหาเฉพาะจุด\n"
            "• Threat: กระแสสินค้าใหม่ใน TikTok อาจกลบตัวนี้ได้\n\n"
            "🎯 Recommendation: เน้นทำคอนเทนต์โชว์ผลลัพธ์ (Before/After) จะปิดการขายได้ดีที่สุดครับ"
        )

class ContentGenerator:
    @staticmethod
    def generate(brand: str, style: str):
        styles = {
            "review": "🔥 รีวิวจัดเต็ม! เจาะลึกจุดเด่นแบบใช้จริง...",
            "problem": "⚠️ ปัญหากวนใจคนเลี้ยงสัตว์จะหมดไป ด้วย...",
            "urgent": "🚨 ดีลเด็ดมาไวไปไว! ไอเทมที่คนเลี้ยงสัตว์ต้องรีบมี..."
        }
        return f"📝 [Content Draft: {brand} | Style: {style.upper()}]\n\n{styles.get(style, 'มาดูกันว่าทำไมตัวนี้ถึงขายดี...')}\n\n✅ จุดเด่น: ใช้งานง่าย ปลอดภัย เห็นผลจริงใน 7 วัน\n👉 แชร์เก็บไว้เลยครับ ก่อนดีลจะหมด!"

class PetCareHunter:
    @staticmethod
    async def get_real_deals():
        # เน้นดึงกลุ่มสินค้าเพื่อให้นำเสนอเป็นลิสต์
        data = await SearchEngine.search("สินค้า Pet Care ขายดี Shopee Affiliate 2026")
        return (
            "🐾 [Pet Care Hunter: สรุปรายการสินค้าคัดสรรพิเศษ]\n\n"
            "📋 รายการสินค้าแนะนำประจำวันนี้:\n" + data + "\n\n"
            "💡 พิมพ์ 'analyze [ชื่อสินค้า]' เพื่อวิเคราะห์ หรือ 'write [ชื่อสินค้า] review' เพื่อให้ผมร่าง Content ให้ครับ!"
        )

class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        if "/findpets" in text_lower:
            await Messenger.send("🐾 [Pet Care Hunter: กำลังคัดกรองสินค้าที่ดีที่สุดให้บอส...]")
            report = await PetCareHunter.get_real_deals()
            await Messenger.send(report)
        elif text_lower.startswith("analyze"):
            brand = text.replace("analyze", "").strip()
            await Messenger.send(AnalyzerAgent.run_swot(brand))
        elif text_lower.startswith("write"):
            parts = text.split()
            brand = parts[1] if len(parts) > 1 else "สินค้า"
            style = parts[2] if len(parts) > 2 else "review"
            await Messenger.send(ContentGenerator.generate(brand, style))
        else:
            await Messenger.send("✅ ระบบพร้อมทำงาน:\n- /findpets [สแกนรายการสินค้า]\n- analyze [ชื่อสินค้า]\n- write [ชื่อสินค้า] [style]")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

scheduler = AsyncIOScheduler(timezone=timezone('Asia/Bangkok'))
scheduler.add_job(lambda: asyncio.create_task(Messenger.send("☀️ อรุณสวัสดิ์ครับบอส! ระบบคัดสินค้าพร้อมทำงานครับ")), 'cron', hour=9, minute=0)
scheduler.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))