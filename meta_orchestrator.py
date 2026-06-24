import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

try:
    # ดึงรายการโมเดลที่ใช้งานได้จริงจาก Account ของบอสมาตรวจสอบ
    models = genai.list_models()
    # กรองเอาเฉพาะโมเดลที่รองรับ generateContent
    available_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
    
    if available_models:
        # เลือกตัวแรกที่ใช้ได้เสมอ
        model_name = available_models[0].name
        print(f"Log: ระบบเลือกใช้โมเดล {model_name}")
        model = genai.GenerativeModel(model_name)
    else:
        # กรณีหาไม่เจอจริงๆ ให้ใช้ค่าเริ่มต้น
        model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Log: เกิดข้อผิดพลาดขณะเลือกโมเดล - {e}")
    model = genai.GenerativeModel('gemini-pro')

class MetaOrchestrator:
    async def log_to_sheets(self, product, content):
        sheet_url = os.environ.get("APPS_SCRIPT_URL")
        if not sheet_url: return
        payload = {"product": product, "hook": "AI Generated", "solution": content}
        async with httpx.AsyncClient() as client:
            try:
                await client.post(sheet_url, json=payload, timeout=10.0)
                print(f"Log: ข้อมูลถูกบันทึกลง Sheets สำหรับ {product}")
            except Exception as e:
                print(f"Log Error: บันทึก Sheets พลาด - {e}")

    async def process(self, text):
        msg = text.strip()
        print(f"Log: ได้รับข้อความ '{msg}'") # เช็คว่าได้รับข้อความไหม

        if "analyze" in msg.lower():
            # ... (ส่วนการสแกนสินค้าคงเดิม)
            await self.send_telegram("✅ รายการสินค้า: 1. CAT PILLOW, 2. PET COLLAR, 3. SMART FEEDER")

        elif len(msg) > 2 and "analyze" not in msg.lower():
            await self.send_telegram(f"✍️ คุณอนิศกำลังเขียนคอนเทนต์สำหรับ: {msg}...")
            
            try:
                print("Log: กำลังสั่งให้ Gemini เขียนคอนเทนต์...")
                response = model.generate_content(f"เขียนคอนเทนต์ปิดการขายสั้นๆ สำหรับ: {msg}")
                content = response.text
                print(f"Log: ได้รับคอนเทนต์จาก Gemini ความยาว {len(content)} ตัวอักษร")
                
                await self.send_telegram(f"🚀 [สำเร็จ]:\n\n{content}")
                await self.log_to_sheets(msg, content)
            except Exception as e:
                print(f"Log Error: เกิดปัญหาตอนเขียนคอนเทนต์ - {str(e)}")
                await self.send_telegram("❌ ขออภัยครับ คอนเทนต์มีปัญหา ติดต่อบอสเพื่อเช็ค Log ครับ")

    async def send_telegram(self, text):
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.api_route("/health", methods=["GET", "HEAD"])
async def health(): return Response(status_code=200)

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().process(message))
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))