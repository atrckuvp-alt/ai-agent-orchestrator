# =====================================================================
# 🚀 V21.3.1: STABLE SEQUENTIAL ORCHESTRATOR
# =====================================================================
import os, asyncio, uvicorn, httpx
from fastapi import FastAPI, Request, Response
import google.generativeai as genai

app = FastAPI(title="BU.1_Master_Integrated")

# Config
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# --- 1. Pipeline Engine ---
async def fetch_serper(query):
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key: return []
        
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://google.serper.dev/search", json={"q": query, "num": 5}, headers=headers)
        data = response.json()
        return [item.get("title") for item in data.get("organic", [])]

def validate_product(name):
    return len(name) > 10

def generate_content_brief(name):
    return (f"🔥 [Hook]: กำลังหา {name} อยู่ใช่ไหม?...\n"
            f"✅ [Solution]: แนะนำ {name} ที่เหล่าทาสแมวบอกต่อ!\n"
            f"👉 [CTA]: สั่งด่วนที่ [Link]")

# --- 2. Messenger & Orchestrator ---
class Messenger:
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text})

class MetaOrchestrator:
    async def handle_request(self, text):
        if text.startswith("analyze"):
            query = text.replace("analyze", "").strip() or "อาหารแมว"
            await Messenger.send(f"🔍 [กำลังสแกน]: {query}...")
            
            products = await fetch_serper(query)
            found = False
            for p in products:
                if validate_product(p):
                    brief = generate_content_brief(p)
                    await Messenger.send(f"✅ [พบสินค้าคุณภาพ]:\n\n{brief}")
                    found = True
                    break 
            if not found:
                await Messenger.send("⚠️ ไม่พบสินค้าที่ผ่านเกณฑ์การตรวจสอบครับ")
        else:
            await Messenger.send("✅ ระบบพร้อม: พิมพ์ 'analyze [ชื่อสินค้า]' เพื่อสแกนตลาดครับ")

# --- 3. Routes ---
@app.api_route("/", methods=["GET", "HEAD"])
async def root(): return Response(content="OK", status_code=200)

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    # เปลี่ยนจากการใช้ create_task เป็นการ await ตรงนี้เพื่อให้ Render ประมวลผลจนจบ
    await MetaOrchestrator().handle_request(text)
    return Response(content="OK")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))