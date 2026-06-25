import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# โมเดลตัวเลือกสำรอง หากตัวหลักมีปัญหา
def get_model():
    return genai.GenerativeModel('gemini-1.5-flash')

model = get_model()

class BU1_Orchestrator:
    async def run_bu1_pipeline(self, query):
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY"), "Content-Type": "application/json"}
        # ปรับ Query ให้ดึง Specific Product
        payload = {"q": f"best selling affiliate products for {query} or specific plan name", "num": 10}
        
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            results = resp.json().get("organic", [])
            raw_data = [item.get("title") for item in results if item.get("title")]

        prompt = f"""
        วิเคราะห์ข้อมูลตลาดนี้: {raw_data}
        1. คัดเลือกชื่อสินค้าที่ทำ Affiliate ได้จริงมา 3 รายการ (ระบุชื่อสินค้าเฉพาะเจาะจง ห้ามเป็นชื่อหมวดหมู่)
        2. คัดเลือกของฟรี/เนื้อหาดึงดูดใจมา 1 รายการ
        ส่งผลลัพธ์ในรูปแบบนี้เท่านั้น:
        สินค้า1: [ชื่อสินค้า]
        สินค้า2: [ชื่อสินค้า]
        สินค้า3: [ชื่อสินค้า]
        ของฟรี: [ชื่อของฟรี]
        """
        response = model.generate_content(prompt)
        return response.text

    async def create_content(self, product):
        prompt = f"เขียนคอนเทนต์ขายสินค้า {product} สำหรับทำ Affiliate โดยเน้นจุดเด่นที่ทำให้น่าซื้อทันที"
        response = model.generate_content(prompt)
        return response.text

class MetaOrchestrator:
    def __init__(self):
        self.bu1 = BU1_Orchestrator()
        self.state = {}

    async def process(self, text):
        try:
            msg = text.strip()
            if "analyze" in msg.lower():
                await self.send_telegram("🏢 [CEO คุณศุภจี]: เริ่มกระบวนการ BU.1 คัดกรองสินค้า...")
                query = msg.lower().replace("analyze", "").strip() or "pet care"
                raw_result = await self.bu1.run_bu1_pipeline(query)
                
                # เก็บ state เพื่อรอการเลือกจาก HUMAN
                self.state["last_result"] = raw_result
                await self.send_telegram(f"✅ **[รายงานจาก BU.1]**:\n{raw_result}\n\n👉 *พิมพ์ชื่อสินค้าที่ต้องการ เพื่อให้คุณอนิศเริ่มงาน*")
            
            else:
                # ตรวจสอบว่าข้อความที่พิมพ์มา อยู่ในรายงานที่ส่งไปหรือไม่
                await self.send_telegram(f"✍️ [CEO คุณศุภจี]: รับทราบ! ส่งงานให้คุณอนิศเขียนคอนเทนต์สำหรับ: {msg}")
                content = await self.bu1.create_content(msg)
                await self.send_telegram(f"🚀 **[รายงานจากคุณอนิศ]**:\n\n{content}")
                await self.log_to_sheets(msg, content)
        except Exception as e:
            await self.send_telegram(f"❌ [ระบบแจ้งเตือน]: เกิดข้อผิดพลาดระหว่างทำงาน: {str(e)}")

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