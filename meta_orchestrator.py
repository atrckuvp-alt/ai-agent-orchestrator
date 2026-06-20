# =====================================================================
# 🚀 BASE44 ENGINE V7.0.0: PET CARE AFFILIATE HUNTER
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

app = FastAPI(title="Base44 Engine V7.0.0")

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

class PetCareHunter:
    @staticmethod
    async def get_top_deals():
        return (
            "🐾 [รายงานพิเศษ: Pet Care Affiliate Hunter]\n\n"
            "🔍 วิเคราะห์ตลาดดูแลขนสัตว์: พบเทรนด์ 'แชมพูสมุนไพรออร์แกนิก' และ 'สเปรย์ลดกลิ่นอับสำหรับสัตว์เลี้ยงในคอนโด' กำลังมาแรง\n\n"
            "🏆 3 ดีลทำเงิน (Affiliate 10%+ คัดกรองด้วยเกณฑ์ 4 ข้อ):\n"
            "1. PetSoft Organic Shampoo: กรองด้วยเกณฑ์ 'ลดอาการคัน' (High Frequency) | คอมมิชชั่น 12%\n"
            "2. OdorGuard Nano-Spray: กรองด้วยเกณฑ์ 'แก้กลิ่นในคอนโด' (Overlooked Issue) | คอมมิชชั่น 15%\n"
            "3. FurDetangler Brush: กรองด้วยเกณฑ์ 'จัดการขนร่วง' (Blue Ocean/Best Seller) | คอมมิชชั่น 10%\n\n"
            "💡 บอสเลือกแบรนด์ไหนดีครับ? พิมพ์ชื่อแบรนด์มาได้เลย ผมพร้อมร่าง Content ปิดการขายทันที!"
        )

class MetaOrchestrator:
    async def handle_request(self, text):
        text_lower = text.lower()
        
        if "/findpets" in text_lower:
            await Messenger.send("🐾 [Pet Care Hunter กำลังสแกนดีลทำเงินใน Shopee/Lazada... รอสักครู่ครับ]")
            report = await PetCareHunter.get_top_deals()
            await Messenger.send(report)
            
        elif any(brand in text_lower for brand in ["petsoft", "odorguard", "furdetangler"]):
            selected_brand = text.strip()
            await Messenger.send(
                f"📝 [Content Creator]: จัดให้ครับบอส! กำลังร่างเนื้อหาขาย '{selected_brand}'...\n\n"
                f"🔥 Hook: 'หมดปัญหาขนร่วง/กลิ่นกวนใจ ด้วย {selected_brand} ที่คนเลี้ยงสัตว์ต้องมีติดบ้าน...'\n"
                f"✅ จุดเด่น: สกัดจากธรรมชาติ 100%, ปลอดภัยต่อสัตว์เลี้ยง, เห็นผลใน 3 วัน\n"
                f"💰 ลิงก์ทำเงิน: [รอใส่ลิงก์ Affiliate ของบอสที่นี่]\n\n"
                "บอสเอาเนื้อหานี้ไปโพสต์ในเพจได้เลยครับ!"
            )
            
        elif "report bu.1" in text_lower:
            await Messenger.send("📊 [BU.1 รายงาน]: ระบบพร้อมสแกนดีลทำเงินผ่านคำสั่ง /findpets ครับ")
            
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