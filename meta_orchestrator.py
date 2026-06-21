# =====================================================================
# 🚀 BASE44 ENGINE V9.0.0: FULL STRATEGIC PIPELINE + CONTENT GENERATOR
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V9.0.0")

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

class AnalyzerAgent:
    @staticmethod
    def run_swot(brand_name: str):
        return (
            f"🧠 [Strategic Analysis: {brand_name}]\n\n"
            "📈 S.W.O.T. Snapshot:\n"
            "• Strength: ความถี่ในการใช้สูง (High Frequency)\n"
            "• Weakness: การแข่งขันในตลาดสูง (High Competition)\n"
            "• Opportunity: กลุ่มลูกค้าที่มองหาสินค้าแก้ปัญหาเฉพาะจุด (Blue Ocean)\n"
            "• Threat: การปรับเรตคอมมิชชั่นจากเจ้าของแพลตฟอร์ม\n\n"
            "🎯 Recommendation: บอสควรเน้นทำ Content แบบ 'Before & After' เพื่อแก้ Pain point ของลูกค้าจะปิดการขายได้ไวที่สุดครับ"
        )

class ContentGenerator:
    @staticmethod
    def generate(brand: str, style: str):
        styles = {
            "review": "🔥 รีวิวจัดเต็ม! เจาะลึกจุดเด่นแบบใช้จริง...",
            "problem": "⚠️ ปัญหากวนใจคนเลี้ยงสัตว์จะหมดไป ด้วย...",
            "urgent": "🚨 ดีลเด็ดมาไวไปไว! ไอเทมที่คนเลี้ยงสัตว์ต้องรีบมี..."
        }
        hook = styles.get(style, "มาดูกันว่าทำไมตัวนี้ถึงขายดี...")
        return (
            f"📝 [Content Draft: {brand} | Style: {style.upper()}]\n\n"
            f"{hook}\n\n"
            "✅ จุดเด่น: ใช้งานง่าย ปลอดภัย เห็นผลจริงใน 7 วัน\n"
            "💰 พิกัดกดสั่งตรงนี้: [รอใส่ลิงก์ Affiliate ของบอส]\n\n"
            "👉 แชร์เก็บไว้เลยครับ ก่อนดีลจะหมด!"
        )

class PetCareHunter:
    @staticmethod
    async def get_real_deals():
        data = await SearchEngine.search("สินค้า Pet Care ขายดี Shopee Affiliate คอมมิชชั่นสูง")
        free_samples = await SearchEngine.search("สินค้าสัตว์เลี้ยง แจกฟรี ทดลองใช้ ฟรี Shopee")
        return (
            "🐾 [รายงานพิเศษ: Pet Care Affiliate Hunter (Real-time)]\n\n"
            "🔍 ผลการค้นหาดีลทำเงินในตลาดปัจจุบัน:\n"
            f"{data}\n\n"
            "🎁 [Free Sample Alert: โอกาสทำคอนเทนต์รีวิวฟรี]:\n"
            f"{free_samples}\n\n"
            "💡 คำสั่งที่บอสใช้ได้:\n- analyze [ชื่อแบรนด์] (วิเคราะห์ SWOT)\n- write [ชื่อแบรนด์] [style] (ร่าง Content)"
        )

class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        if "/findpets" in text_lower:
            await Messenger.send("🐾 [Pet Care Hunter กำลังสแกนดีลจริง...]")
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
        elif "report bu.1" in text_lower:
            await Messenger.send("📊 [BU.1 รายงาน]: ระบบพร้อมสแกนดีล, วิเคราะห์ S.W.O.T. และร่าง Content ครับ")
        else:
            await Messenger.send("✅ ระบบพร้อมทำงาน:\n- /findpets [สแกนดีล]\n- analyze [ชื่อแบรนด์] [วิเคราะห์]\n- write [แบรนด์] [style] [ร่าง Content]")

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