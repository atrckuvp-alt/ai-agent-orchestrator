# =====================================================================
# 🚀 BASE44 ENGINE V5.4.3: CONSOLE LOGGING & LIVE STREAM EDITION
# =====================================================================
import os
import sys
import json
import datetime
import random
import asyncio
from typing import List, Dict, Any, Optional
import uvicorn
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="Base44 Engine V5.4.3 - Console Logging")

SYSTEM_STATE = {
    "active_ai_model": "GPT-4o (Legacy Base Tier)",
    "bu1_pipeline_status": "PROACTIVE_RUNNING",
    "last_action": "SYSTEM_INITIALIZED",
    "latest_live_report": {}
}

@app.middleware("http")
async def render_redirect_immunity_shield(request: Request, call_next):
    if request.url.path in ["/", ""]:
        if request.method in ["POST", "PUT", "DELETE"]:
            return JSONResponse(status_code=200, content={
                "status": "success",
                "system_state": SYSTEM_STATE
            })
    return await call_next(request)

@app.get("/health")
async def health_check_get(): return {"status": "healthy", "engine_version": "V5.4.3-Log"}

class BU1AutonomousRevenueEngine:
    async def run_pipeline(self) -> dict:
        return {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "product_name": "เซรั่มริ้วรอยทองคำ 24K เมือกหอยทากเกาหลี",
            "commission": "25% - 32%"
        }

@app.get("/", response_class=HTMLResponse)
async def homepage_get():
    return f"""<html><body style="font-family:sans-serif;background:#0f172a;color:#e2e8f0;text-align:center;padding:50px;">
    <h1 style="color:#38bdf8;">🏎️ Base44 Engine V5.4.3</h1>
    <p style="color:#4ade80;">สถานะระบบ: ONLINE (ยิง Log ตรงเข้าคอนโซล Render แล้ว)</p>
    <a href="/test-telegram-report" style="background:#38bdf8;color:#0f172a;padding:10px 20px;text-decoration:none;border-radius:5px;font-weight:bold;">🔥 คลิกเพื่อทดสอบบังคับยิงทันที</a>
    </body></html>"""

@app.get("/api/latest-report")
async def get_latest_report():
    if not SYSTEM_STATE["latest_live_report"]:
        SYSTEM_STATE["latest_live_report"] = await BU1AutonomousRevenueEngine().run_pipeline()
    return {"status": "success", "data": SYSTEM_STATE["latest_live_report"]}

# 🛡️ ท่อรองรับทราฟฟิกจากตัวตั้งเวลาภายนอกทุกๆ 5 นาที
@app.get("/test-telegram-report")
@app.get("/cron")
@app.get("/send-report")
@app.get("/api/cron")
async def test_telegram_report():
    try:
        data = await BU1AutonomousRevenueEngine().run_pipeline()
        SYSTEM_STATE["latest_live_report"] = data
        
        report_text = (
            f"[BASE44 V5.4.3 - Morning Briefing]\n"
            f"ระบบทำงานปกติครับบอส!\n"
            f"สินค้าหลัก: {data['product_name']}\n"
            f"ค่าคอมมิชชั่น: {data['commission']}\n"
            f"เวลาเซิร์ฟเวอร์: {data['timestamp']}"
        )
        
        raw_tokens = os.environ.get("TELEGRAM_BOT_TOKENS", os.environ.get("TELEGRAM_BOT_TOKEN", ""))
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip().replace('"', '').replace("'", "")
        token_list = [t.strip().replace('"', '').replace("'", "") for t in raw_tokens.split(",") if t.strip()]
        
        # 📢 [PRINT 1] พ่นค่า ENV ที่ระบบอ่านได้ออกหน้าจอ Log ทันที
        print(f"\n╔════════════════ TELEGRAM SYNC START ════════════════╗")
        print(f"⏰ เวลาเปิดสเปก: {data['timestamp']}")
        print(f"📊 จำนวนคีย์ที่พบ: {len(token_list)} ชุด")
        print(f"🎯เป้าหมาย CHAT ID: {chat_id}")
        
        if not token_list or not chat_id:
            print("❌ [ERROR] ตรวจพบค่าว่างเปล่าใน ENV ของ Render!")
            print(f"╚═════════════════════════════════════════════════════╝\n")
            return {"status": "error", "reason": "ENV_EMPTY"}

        telegram_status = "❌ ล้มเหลวทั้งหมด"
        
        async with httpx.AsyncClient() as client:
            for index, token in enumerate(token_list):
                if token.lower().startswith("bot"):
                    token = token[3:]
                    
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                payload = {"chat_id": chat_id, "text": report_text}
                
                print(f"🔄 กำลังยิงด้วยคีย์ชุดที่ {index+1} -> {url[:35]}...")
                
                try:
                    response = await client.post(url, json=payload, timeout=12.0)
                    
                    # 📢 [PRINT 2] พ่นคำฟ้องตัวจริงจาก Telegram ลงหน้าคอนโซล Render ตรงๆ!
                    print(f"📡 [TELEGRAM RESPONSE] ตัวจริงตอบกลับมาว่า:")
                    print(f"   -> HTTP STATUS: {response.status_code}")
                    print(f"   -> BODY: {response.text}")
                    
                    if response.status_code == 200:
                        telegram_status = f"✅ สำเร็จด้วยคีย์ชุดที่ {index+1}"
                        break
                except Exception as net_err:
                    print(f"💥 พังระดับ Network กับคีย์ชุดที่ {index+1}: {str(net_err)}")
                    
        print(f"🏁 บทสรุปการส่ง: {telegram_status}")
        print(f"╚═════════════════════════════════════════════════════╝\n")
        
        # ตอบกลับ 200 เสมอเพื่อให้ระบบลื่นไหล แต่เราไปดูเนื้อหาจริงใน Log เอา
        return {"status": "processed", "telegram_delivery": telegram_status}
        
    except Exception as e:
        print(f"🚨 [CRITICAL ERROR]: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)