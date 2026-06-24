import os, asyncio, uvicorn, httpx, json
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI(title="BU.1_Master_Command_Center")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- 1. System Modules (Agents) ---
class Messenger:
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text})
            except Exception as e: print(f"Telegram Error: {e}")

# --- 2. Master Orchestrator (CEO คุณศุภจี) ---
class MetaOrchestrator:
    async def handle_request(self, text):
        msg = text.lower()
        
        # [BU.1 Logic]: สแกนและรายงาน
        if msg.startswith("analyze"):
            query = msg.replace("analyze", "").strip() or "อาหารแมว"
            await Messenger.send(f"🔍 ดร.แสงสุข (Orchestrator) กำลังสแกนหมวด: {query}...")
            
            # ดึงข้อมูลสินค้าจาก Research Agent
            products = await self.fetch_serper(query)
            
            if products:
                # รายงานสินค้า 3 รายการตามที่บอสกำหนด
                report = "✅ [รายงานจาก BU.1 ส่วนที่ 1]: รายการสินค้าแนะนำ 3 รายการ\n\n"
                for i, p in enumerate(products[:3], 1):
                    report += f"{i}. {p}\n"
                report += "\n(พิมพ์ชื่อสินค้าเพื่อสั่งให้คุณอนิศ Content Agent เริ่มทำงานครับ)"
                await Messenger.send(report)
            else:
                await Messenger.send("⚠️ ไม่พบข้อมูลในหมวดนี้")

        # [BU.1 Logic]: Content Agent ทำงาน
        elif any(x in msg for x in ["ของใช้", "อาหาร", "แปรง"]): # สมมติการเลือกสินค้า
            await Messenger.send("✍️ คุณอนิศ (Content Agent) กำลังเขียนคอนเทนต์ปิดการขาย...")
            # ดึง Logic จากการเทสในเครื่องมาใส่ตรงนี้
            await Messenger.send(f"🚀 [สำเร็จ]: คอนเทนต์พร้อมสำหรับ {msg} [ใส่ Affiliate Link ของบอสที่นี่]")
            
        else:
            await Messenger.send("✅ ระบบพร้อม: พิมพ์ 'analyze [หมวดสินค้า]' เพื่อเริ่มงานครับ")

    async def fetch_serper(self, query):
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://google.serper.dev/search", json={"q": query, "num": 5}, headers=headers)
            return [item.get("title") for item in resp.json().get("organic", [])]

# --- 3. Routes ---
@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK")

@app.api_route("/health", methods=["GET", "HEAD"])
async def health(): return Response(content="OK", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))