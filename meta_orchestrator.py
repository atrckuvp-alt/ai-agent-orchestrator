import os, json
from fastapi import FastAPI, Request, Response
import uvicorn, httpx, asyncio

app = FastAPI()

# --- Route พิเศษสำหรับ Render/UptimeRobot (ป้องกัน 404) ---
@app.api_route("/", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def root(): return Response(content="OK", status_code=200)

@app.api_route("/health", methods=["GET", "POST", "HEAD", "OPTIONS"])
async def health(): return Response(content="OK", status_code=200)

# --- Memory System ---
HISTORY_FILE = "product_history.json"
def load_history():
    if not os.path.exists(HISTORY_FILE): return {}
    with open(HISTORY_FILE, "r") as f: return json.load(f)

def save_history(product, data):
    h = load_history()
    h[product] = data
    with open(HISTORY_FILE, "w") as f: json.dump(h, f, indent=4)

@app.post("/telegram-webhook")
async def handle(request: Request):
    data = await request.json()
    text = data.get("message", {}).get("text", "").lower()
    
    if text.startswith("analyze"):
        product = text.replace("analyze", "").strip()
        history = load_history()
        
        if product in history:
            msg = f"🧠 Memory Found: {history[product]}"
        else:
            save_history(product, "ข้อมูลวิเคราะห์ฉบับสมบูรณ์")
            msg = f"🧠 New Item! บันทึก {product} ลง Memory แล้วครับ"
        
        await httpx.AsyncClient().post(
            f"https://api.telegram.org/bot8929890944:AAHuJ1xcMjWskVfmH-Ny98Qjwf7kiXgb--4/sendMessage",
            json={"chat_id": "7238952711", "text": msg}
        )
    return Response(content="OK", status_code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)