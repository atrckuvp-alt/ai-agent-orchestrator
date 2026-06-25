import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BU.1 Agent System ---
class BU1_Orchestrator:
    async def analyze_market(self, query):
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        payload = {"q": f"trending products for {query} high conversion", "num": 5}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            results = resp.json().get("organic", [])
            # Marketing Agent (คุณสิทธินันท์) คัดเลือก 3 รายการ
            return [item.get("title") for item in results[:3]]

    async def create_content(self, product):
        prompt = f"เขียนคอนเทนต์ขายสินค้า: {product} โดยเน้น Hidden Pain Points และกลยุทธ์ปิดการขาย Affiliate"
        response = model.generate_content(prompt)
        return response.text

# --- CEO: Meta-Orchestrator (คุณศุภจี) ---
class MetaOrchestrator:
    def __init__(self):
        self.bu1 = BU1_Orchestrator()
        self.state = {}

    async def process(self, text):
        msg = text.strip()
        
        # 1. รับคำสั่ง Analyze -> จ่ายงาน BU.1
        if "analyze" in msg.lower():
            query = msg.lower().replace("analyze", "").strip() or "pet care"
            await self.send_telegram(f"🏢 [CEO คุณศุภจี]: รับคำสั่งแล้ว! ส่งต่อให้ดร.แสงสุขและทีม BU.1 เริ่มสแกน {query}...")
            
            products = await self.bu1.analyze_market(query)
            self.state["products"] = products
            
            reply = "✅ **[รายงานจาก BU.1]**\nดร.แสงสุขและคุณสิทธินันท์คัดเลือกสินค้ามาให้ 3 รายการ:\n"
            reply += "\n".join([f"{i+1}. {p}" for i, p in enumerate(products)])
            await self.send_telegram(f"{reply}\n\n👉 *พิมพ์ชื่อสินค้าที่ต้องการ เพื่อให้คุณอนิศดำเนินการต่อ*")

        # 2. รับสินค้าจากบอส -> จ่ายงานคุณอนิศ (Content Agent)
        elif msg in self.state.get("products", []):
            await self.send_telegram(f"✍️ [CEO คุณศุภจี]: รับทราบครับ ส่งต่อให้คุณอนิศวิเคราะห์และเขียนคอนเทนต์สำหรับ {msg}...")
            content = await self.bu1.create_content(msg)
            await self.send_telegram(f"🚀 **[รายงานความสำเร็จจากคุณอนิศ]**\n\n{content}")
            
            # บันทึกลง Sheets
            await self.log_to_sheets(msg, content)

    async def log_to_sheets(self, product, content):
        sheet_url = os.environ.get("APPS_SCRIPT_URL")
        if not sheet_url: return
        payload = {"product": product, "hook": "AI Generated", "solution": content}
        async with httpx.AsyncClient() as client:
            try: await client.post(sheet_url, json=payload, timeout=10.0)
            except: pass

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

# --- Web Server Routes ---
@app.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
@app.api_route("/health", methods=["GET", "HEAD", "OPTIONS"])
async def root(): return Response(status_code=200, content="OK")

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))