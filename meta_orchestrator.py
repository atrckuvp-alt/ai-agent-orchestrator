import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
# แก้บรรทัดเดิมจาก model = ... เป็นตัวนี้ครับ
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

class MetaOrchestrator:
    # ฟังก์ชันส่งข้อมูลเข้า Google Sheets (เชื่อมต่อ Apps Script)
    async def log_to_sheets(self, product, content):
        sheet_url = os.environ.get("APPS_SCRIPT_URL")
        if not sheet_url: 
            print("⚠️ ไม่พบ APPS_SCRIPT_URL ใน Environment")
            return
        
        # จัดโครงสร้างให้ตรงกับ code ใน Apps Script ของบอส
        payload = {
            "product": product,
            "hook": "AI Generated Content",
            "solution": content
        }
        
        try:
            async with httpx.AsyncClient() as client:
                await client.post(sheet_url, json=payload, timeout=10.0)
        except Exception as e:
            print(f"❌ ส่งข้อมูลเข้า Sheets พลาด: {e}")

    async def process(self, text):
        msg = text.strip()
        
        # ส่วนที่ 1: รับคำสั่งสแกน
        if "analyze" in msg.lower():
            query = msg.lower().replace("analyze", "").strip() or "ทั่วไป"
            await self.send_telegram(f"🔍 ดร.แสงสุข กำลังสแกนหมวด: {query}...")
            
            # (จำลองการสแกนสินค้า)
            products = ["CAT PILLOW", "PET COLLAR", "SMART FEEDER"]
            await self.send_telegram(f"✅ รายการสินค้าที่พบ:\n1. {products[0]}\n2. {products[1]}\n3. {products[2]}\n\n(พิมพ์ชื่อสินค้าเพื่อรับคอนเทนต์ปิดการขายครับ)")

        # ส่วนที่ 2: รับชื่อสินค้าเพื่อสร้าง Content และบันทึก
        elif len(msg) > 2 and "analyze" not in msg.lower():
            await self.send_telegram(f"✍️ คุณอนิศกำลังเขียนคอนเทนต์สำหรับ: {msg}...")
            
            # ใช้ AI สร้าง Content
            response = model.generate_content(f"เขียนคอนเทนต์ปิดการขายที่ดึงดูดใจสำหรับ: {msg}")
            content = response.text
            
            # ส่งผลลัพธ์ไปที่ Telegram
            await self.send_telegram(f"🚀 [สำเร็จ]: คอนเทนต์สำหรับ {msg}\n\n{content}")
            
            # ส่งข้อมูลไปบันทึกที่ Google Sheets
            await self.log_to_sheets(msg, content)

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text}
            )

@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return {"status": "BU.1 Enterprise Ready"}

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))