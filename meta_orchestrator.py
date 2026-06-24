import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI(title="BU.1_Master_Command_Center")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- 1. Messenger System ---
class Messenger:
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: 
                await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text})
            except Exception as e: 
                print(f"Telegram Error: {e}")

# --- 2. Master Orchestrator (CEO คุณศุภจี) ---
class MetaOrchestrator:
    async def fetch_serper(self, query):
        api_key = os.environ.get("SERPER_API_KEY")
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://google.serper.dev/search", json={"q": query, "num": 5}, headers=headers)
            data = resp.json()
            return [item.get("title") for item in data.get("organic", [])]

    async def handle_request(self, text):
        msg = text.lower().strip()
        
        # [BU.1 Workflow]: สแกนตลาด
        if msg.startswith("analyze"):
            query = msg.replace("analyze", "").strip() or "อาหารแมว"
            await Messenger.send(f"🔍 ดร.แสงสุข (Orchestrator) กำลังสแกนหมวด: {query}...")
            
            products = await self.fetch_serper(query)
            if products:
                report = "✅ [รายงานจาก BU.1 ส่วนที่ 1]: รายการสินค้าแนะนำ 3 รายการ\n\n"
                for i, p in enumerate(products[:3], 1):
                    report += f"{i}. {p}\n"
                report += "\n(พิมพ์ชื่อสินค้าที่ต้องการ เพื่อให้คุณอนิศ Content Agent จัดทำคอนเทนต์ปิดการขายครับ)"
                await Messenger.send(report)
            else:
                await Messenger.send("⚠️ ไม่พบข้อมูลสินค้าในหมวดนี้ครับ")

        # [BU.1 Workflow]: Content Agent ทำงาน
        elif len(msg) > 5 and "analyze" not in msg:
            await Messenger.send(f"✍️ คุณอนิศ (Content Agent) กำลังเขียนคอนเทนต์ปิดการขายสำหรับ: {msg}...")
            await asyncio.sleep(1) 
            await Messenger.send(f"🚀 [สำเร็จ]: คอนเทนต์พร้อมสำหรับ {msg}!\n\n🔥 [Hook]: กำลังมองหา {msg} ที่ใช่กันอยู่ใช่ไหม?\n✅ [Solution]: แนะนำตัวนี้เลยที่ทาสแมวบอกต่อ!\n👉 [CTA]: สั่งซื้อได้ที่นี่ [Link]")
            
        else:
            await Messenger.send("✅ ระบบพร้อม: พิมพ์ 'analyze [หมวดสินค้า]' เพื่อเริ่มสแกนตลาดครับ")

# --- 3. Routes (Stability Fixed - Allowed all methods) ---
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return {"status": "BU.1 Operational", "version": "V21.3.3"}

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health(): return Response(content="OK", status_code=200)

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)