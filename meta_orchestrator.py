import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BU.1 Agent System ---
class BU1_Orchestrator:
    async def run_bu1_pipeline(self, query):
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        
        # ดึงข้อมูลสินค้า + ของฟรีในหมวดเดียวกัน
        payload = {"q": f"best selling affiliate products for {query} and free alternatives", "num": 10}
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            results = resp.json().get("organic", [])
            raw_data = [item.get("title") for item in results if item.get("title")]

        # ให้ AI สกัดรายชื่อสินค้า 3 ตัว + ของฟรี 1 ตัว (ตามเงื่อนไขรายงาน BU.1 ส่วน 1 และ 2)
        prompt = f"""
        วิเคราะห์ข้อมูล: {raw_data}
        1. คัดเลือกชื่อสินค้าที่ทำ Affiliate ได้ดีที่สุดมา 3 รายการ
        2. คัดเลือกของฟรีหรือเนื้อหาดึงดูดใจในหมวดเดียวกันมา 1 รายการ
        ตอบเฉพาะชื่อเท่านั้นแยกบรรทัด
        """
        response = model.generate_content(prompt)
        items = [line.strip().lstrip('123456789. ') for line in response.text.split('\n') if line.strip()]
        
        return {"products": items[:3], "free_item": items[3] if len(items) > 3 else "ไม่พบข้อมูลของฟรี"}

    async def create_content(self, product):
        prompt = f"เขียนคอนเทนต์ขายสินค้า {product} พร้อมกลยุทธ์ปิดการขาย Affiliate"
        response = model.generate_content(prompt)
        return response.text

# --- CEO: คุณศุภจี ---
class MetaOrchestrator:
    def __init__(self):
        self.bu1 = BU1_Orchestrator()
        self.state = {}

    async def process(self, text):
        msg = text.strip()
        
        if "analyze" in msg.lower():
            query = msg.lower().replace("analyze", "").strip() or "pet care"
            await self.send_telegram(f"🏢 [CEO คุณศุภจี]: ส่งงานให้ ดร.แสงสุข และ คุณสิทธินันท์ ตรวจสอบตลาด...")
            
            data = await self.bu1.run_bu1_pipeline(query)
            self.state["products"] = data["products"]
            
            reply = "✅ **[รายงานจาก BU.1 ส่วนที่ 1]**\nรายการสินค้าที่คัดสรรแล้ว:\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(data["products"])])
            reply += f"\n\n🎁 **[รายงานจาก BU.1 ส่วนที่ 2]**\nของฟรีที่สืบหามาได้: {data['free_item']}"
            await self.send_telegram(f"{reply}\n\n👉 *พิมพ์ชื่อสินค้าที่ต้องการ เพื่อให้คุณอนิศดำเนินการต่อ*")

        elif msg in self.state.get("products", []):
            await self.send_telegram(f"✍️ [CEO คุณศุภจี]: ส่งให้คุณอนิศวิเคราะห์และเขียนคอนเทนต์สำหรับ {msg}...")
            content = await self.bu1.create_content(msg)
            await self.send_telegram(f"🚀 **[รายงานจากคุณอนิศ]**\n\n{content}")
            await self.log_to_sheets(msg, content)

    async def log_to_sheets(self, product, content):
        sheet_url = os.environ.get("APPS_SCRIPT_URL")
        if not sheet_url: return
        async with httpx.AsyncClient() as client:
            try: await client.post(sheet_url, json={"product": product, "solution": content}, timeout=10.0)
            except: pass

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

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