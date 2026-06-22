# =====================================================================
# 🚀 BU.1 & BU.2 UNIFIED MASTER SYSTEM (V18.0.0)
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response

app = FastAPI(title="BU.1_BU.2_Master_System")

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

# --- BU.1 Engine: Pet Care & Affiliate ---
class BU1_Engine:
    @staticmethod
    async def run_pipeline():
        # จำลองการทำงานของ ดร.แสงสุข และ คุณสิทธินันท์ [cite: 6, 8, 9]
        return (
            "🏢 [คุณศุภจี]: รายงานผลจากทีม BU.1 ครับ [cite: 7]\n\n"
            "🔎 [ดร.แสงสุข]: คัดกรอง 3 สินค้า Pet Care ศักยภาพสูงมาให้แล้วครับ [cite: 8]\n"
            "📊 [คุณสิทธินันท์]: พร้อมผล Market Viability Score [cite: 9]\n"
            "1. อาหารเสริมขนสวย | Score: 9.2/10\n"
            "2. ทรายแมวสูตรย่อยสลาย | Score: 8.8/10\n"
            "3. ขนมขัดฟันออร์แกนิก | Score: 8.5/10\n\n"
            "🎁 [ส่วนที่ 2]: ของฟรี/สินค้าทดลอง: อาหารแมวสูตรเปียก (ขนาดทดลอง) สำหรับดึงคนเข้า Page [cite: 17]\n\n"
            "🧠 [คุณอนิศ]: บอสเลือกสินค้า 1 รายการ แล้วสั่ง 'analyze [ชื่อสินค้า]' ให้ผมขยี้ Pain Point ต่อได้เลยครับ! [cite: 10, 16]"
        )

# --- BU.2 Engine: AI Sourcing ---
class BU2_Engine:
    @staticmethod
    async def run_pipeline():
        # ทำงานตาม Workflow ของ Research & Coding Agent [cite: 14, 15]
        return (
            "🏢 [คุณศุภจี]: รายงานจากทีม BU.2 ครับ [cite: 12]\n\n"
            "🔍 [Research Agent]: พบ AI Open-source Free-tier 100% ตัวใหม่ด้าน Research ประสิทธิภาพสูงกว่าตัวเดิม ขออนุมัติใช้งานแทนครับ [cite: 14, 19]\n\n"
            "💻 [Coding Agent]: พบ AI Open-source Free-tier 100% ด้าน Coding ประสิทธิภาพสูงกว่าตัวเดิม ผ่านการตรวจเช็คจาก Research Agent แล้ว ขออนุมัติใช้งานแทนครับ [cite: 15, 20]\n\n"
            "👉 บอสพิจารณาอนุมัติ พิมพ์ 'approve [ชื่อ AI]' เพื่อเปลี่ยนตัวใช้งานครับ!"
        )

# --- Meta-Orchestrator: CEO Center ---
class MetaOrchestrator:
    async def handle_request(self, text):
        command = text.lower()
        if "petcare" in command:
            await Messenger.send("🏢 [คุณศุภจี]: รับทราบครับ งาน Pet Care จ่ายให้ BU.1 ดำเนินการ [cite: 3, 7]")
            report = await BU1_Engine.run_pipeline()
            await Messenger.send(report)
        elif "findai" in command:
            await Messenger.send("🏢 [คุณศุภจี]: รับทราบครับ งานสืบหา AI จ่ายให้ BU.2 ดำเนินการ [cite: 3, 12]")
            report = await BU2_Engine.run_pipeline()
            await Messenger.send(report)
        else:
            await Messenger.send("✅ ระบบพร้อม:\n- พิมพ์ 'petcare' สำหรับ BU.1 [cite: 6]\n- พิมพ์ 'findai' สำหรับ BU.2 [cite: 11]")

@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)