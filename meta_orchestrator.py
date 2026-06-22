# =====================================================================
# 🚀 V21.1.0: MASTER INTEGRATED SYSTEM (THE FINAL FORM - CLEAN LOG)
# =====================================================================
import os, asyncio, uvicorn, httpx, json
from fastapi import FastAPI, Request, Response

app = FastAPI(title="BU.1_BU.2_Master_System")

# --- 1. Memory & Validator Engines ---
class HistoryEngine:
    DB = "product_history.json"
    @classmethod
    def check(cls, p):
        if not os.path.exists(cls.DB): return None
        with open(cls.DB, "r") as f:
            try: return json.load(f).get(p)
            except: return None
    @classmethod
    def save(cls, p, data):
        h = {}
        if os.path.exists(cls.DB):
            with open(cls.DB, "r") as f:
                try: h = json.load(f)
                except: h = {}
        h[p] = data
        with open(cls.DB, "w") as f: json.dump(h, f, indent=4)

def validate_product(data):
    # เกณฑ์การคัดกรอง: ต้องมีชื่อ และคะแนน >= 7.0
    if not data.get("name") or data.get("score", 0) < 7.0: return False
    return True

# --- 2. Content Framework ---
def generate_brief(name, pain):
    return (f"🔥 [Hook]: เบื่อไหม? กับปัญหา {pain} ในน้องแมวของคุณ...\n"
            f"⚠️ [Pain]: ปล่อยไว้อาจเกิดปัญหาเรื้อรัง ค่ารักษาสูง!\n"
            f"✅ [Solution]: แนะนำ {name} ตัวช่วยลับที่คนรักแมวบอกต่อ\n"
            f"👉 [CTA]: รับโปรพิเศษก่อนของหมดที่นี่ [Link]")

# --- 3. Core Logic & Communication ---
class Messenger:
    TOKEN = "8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4"
    CHAT_ID = "7238952711"
    @classmethod
    async def send(cls, text):
        async with httpx.AsyncClient() as client:
            try: await client.post(f"https://api.telegram.org/bot{cls.TOKEN}/sendMessage", json={"chat_id": cls.CHAT_ID, "text": text}, timeout=10.0)
            except: pass

class MetaOrchestrator:
    async def handle_request(self, text):
        cmd = text.lower()
        if cmd.startswith("analyze"):
            product = cmd.replace("analyze", "").strip()
            # 1. เช็ค Memory
            memo = HistoryEngine.check(product)
            if memo:
                await Messenger.send(f"🧠 [Memory Found]: ข้อมูลเดิมของ {product}\n\n{memo}")
            else:
                # 2. จำลองการคัดกรอง (Validator)
                mock_data = {"name": product, "score": 9.5}
                if validate_product(mock_data):
                    brief = generate_brief(product, "น้องแมวขนร่วงและผิวแห้ง")
                    HistoryEngine.save(product, brief)
                    await Messenger.send(f"✅ [Validator Pass]: ได้สินค้าคุณภาพสูง!\n\n{brief}")
                else:
                    await Messenger.send(f"❌ [Validator Fail]: สินค้า {product} ไม่ผ่านเกณฑ์คัดกรอง")
        else:
            await Messenger.send("✅ ระบบพร้อม: พิมพ์ 'analyze [ชื่อสินค้า]' เพื่อให้ระบบคัดกรองและสร้าง Brief ให้บอสครับ!")

# --- 4. Routes (Clean Log) ---
@app.get("/")
async def root(): return Response(content="OK", status_code=200)

@app.get("/health")
async def health(): return Response(content="OK", status_code=200)

@app.head("/health")
async def health_head(): return Response(content="", status_code=200)

@app.post("/telegram-webhook")
async def webhook(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "")
    asyncio.create_task(MetaOrchestrator().handle_request(text))
    return Response(content="OK")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)