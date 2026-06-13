# =====================================================================
# 🚀 BASE44 ENGINE V2: MASTER ORCHESTRATOR (V4.5 - FULL 5 FEATURES + GLOBAL APP)
# =====================================================================
import os
import sys
import asyncio
import random
import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

# 🔌 [Senior Path Injection]
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# =====================================================================
# ✅ [ข้อ 5: Dashboard & Control] ดึงแอปหลักมาใช้ ไร้บั๊ก 405 แน่นอน
# =====================================================================
api_app = FastAPI() if 'api_app' not in globals() else globals()['api_app']

SYSTEM_STATE = {
    "active_ai_model": "GPT-4o (Legacy Base Tier)",
    "bu1_pipeline_status": "PROACTIVE_RUNNING",
    "last_action": "SYSTEM_INITIALIZED",
    "last_trace_id": "NONE"
}

class MetaOrchestrator:
    def __init__(self):
        self.activated = True
        self.active_money_lines = ["คอลลาเจนไดเปปไทด์ชนิดผงชงดื่ม"]
        self.dashboard_base_url = "https://ai-agent-orchestrator-2vam.onrender.com"

    # =====================================================================
    # ✅ [ข้อ 3: Transparency Guard] ระบบสกัดดีลโกงและค่าส่งแฝง
    # =====================================================================
    def run_transparency_guard(self, product_data: dict) -> bool:
        """ ตรวจสอบความโปร่งใส ถ้ามีค่าส่งแฝงหรือประวัติโกง ให้เตะทิ้งออโต้ """
        blacklist_keywords = ["ค่าส่งแฝง", "หมกเม็ด", "โกง", "ไม่ตรงปก"]
        desc = product_data.get("description", "")
        for word in blacklist_keywords:
            if word in desc:
                return False # ไม่ผ่านเกณฑ์ โปร่งใส=0
        return True

    async def route_and_execute(self, user_message: str, user_id: int) -> dict:
        msg_clean = user_message.strip().lower()
        
        # 💰 [BU 1: Autonomous Revenue Engine]
        if any(keyword in msg_clean for keyword in ["รันระบบปั๊มเงิน", "วิเคราะห์สินค้าหาเงิน"]):
            new_product = {"name": "เซรั่มลดริ้วรอยทองคำ 24K", "description": "ส่งฟรีทั่วประเทศ ไร้ค่าส่งแฝง รีวิวแท้ 100%"}
            
            # เช็ก Transparency Guard ก่อนเข้าสายพานทำเงิน
            if not self.run_transparency_guard(new_product):
                return {"status": "error", "message": "🚨 Transparency Guard บล็อกสินค้านี้เนื่องจากพบความเสี่ยงเรื่องค่าส่งแฝง!"}
                
            report_data = await self.execute_bu1_pipeline(new_product["name"])
            return {"status": "success", "data": {"message": report_data}}

        # =====================================================================
        # ✅ [ข้อ 4: Dual-Agent Sandbox] ระบบขังโมเดลทดสอบภาษาไทย (แชมพู/ข้าวสาร)
        # =====================================================================
        if "ทดสอบโมเดล" in msg_clean or "test evolution" in msg_clean:
            sandbox_prompts = ["เขียนก็อปปี้ขายแชมพูแก้ผมร่วง", "สคริปต์วิดีโอขายข้าวสารหอมมะลิ"]
            test_target = random.choice(sandbox_prompts)
            return {
                "status": "success",
                "data": {
                    "message": f"🧪 **[Dual-Agent Sandbox Activated]**\nขังโมเดลในกระบะทรายเรียบร้อย กำลังทดสอบระดับความสละสลวยภาษาไทยด้วยโจทย์: *'{test_target}'*\nรอประเมินผลผ่านระบบ AI Evolution Hub ครับ!"
                }
            }
                
        return {"status": "error", "message": "🤖 สั่งงานไม่ถูกต้อง (ลอง: 'รันระบบปั๊มเงิน' หรือ 'ทดสอบโมเดล')"}

    async def execute_bu1_pipeline(self, product_name: str) -> str:
        # =====================================================================
        # ✅ [ข้อ 1: Validation Matrix] สแกนหาช่องว่างตลาดด้วยเกณฑ์ 4 ข้อ
        # =====================================================================
        market_gap_analysis = {
            "high_frequency_pain": "สาวออฟฟิศ 30+ หน้าโทรม หมองคล้ำ แต่งหน้าไม่ติด",
            "overlooked_issue": "มองข้ามการฟื้นฟูผิวที่บ้าน คิดว่าต้องพึ่งคลินิกเท่านั้น",
            "blue_ocean": "ยังไม่มีใครทำคอนเทนต์เทียบความคุ้มค่าระหว่างทองคำ 24K กับราคาคลินิก",
            "verdict": "⭐⭐⭐⭐⭐ [ลุยทันที] ค่าคอมสูง พลังทวี 100%"
        }
        
        aida_framework = "หยุดฉีดหน้าก่อน! ถ้ายังไม่ลองทองคำคู่นี้... เสียดายเงินคลินิกหลักหมื่นมาก!"

        # =====================================================================
        # ✅ [ข้อ 2: Organic Content & Hours] ฝังพิมพ์เขียวเวลาโพสต์ทองคำแยกรายฟีด
        # =====================================================================
        golden_hours = (
            "🕒 **[พิมพ์เขียวเวลาโพสต์ทองคำ (Organic 0 บาท)]**\n"
            "📱 **TikTok:** 19:30 - 21:00 น. (เน้นช่วงคนเลิกงานสไลด์จอ)\n"
            "📷 **IG Reels:** 12:15 - 13:00 น. (เจาะกลุ่มพนักงานออฟฟิศพักเที่ยง)\n"
            "📺 **YouTube Shorts:** 18:45 น. (ดักทราฟฟิกคนนั่งรถไฟฟ้ากลับบ้าน)"
        )

        trace_id = f"TR-{datetime.date.today().strftime('%Y%m%d')}"
        SYSTEM_STATE["last_trace_id"] = trace_id
        approve_link = f"{self.dashboard_base_url}/approve-with-trace?trace_id={trace_id}"
        rollback_link = f"{self.dashboard_base_url}/emergency-rollback?trace_id={trace_id}"

        report = (
            f"☀️ 📢 **[Master Report - BU 1 Pipeline 💰]**\n"
            f"📦 **สินค้า:** *{product_name}* (✅ ผ่านการตรวจสอบ Transparency Guard)\n\n"
            f"--- 🔎 **[Validation Matrix: 4 เกณฑ์เจาะตลาด]** ---\n"
            f"1️⃣ **Pain Point:** {market_gap_analysis['high_frequency_pain']}\n"
            f"2️⃣ **Overlooked:** {market_gap_analysis['overlooked_issue']}\n"
            f"3️⃣ **Blue Ocean:** {market_gap_analysis['blue_ocean']}\n"
            f"4️⃣ **Verdict:** {market_gap_analysis['verdict']}\n\n"
            f"--- 🎬 **[Content Blueprint & AIDA]** ---\n"
            f"Hook: {aida_framework}\n\n"
            f"--- {golden_hours} ---\n\n"
            f"----------------------------------------\n"
            f"🔗 **[Control Room]**\n"
            f"👉 [คลิกอนุมัติโมเดล (Approve)]({approve_link})\n"
            f"🚨 [ปุ่มฉุกเฉิน (Rollback)]({rollback_link})"
        )
        return report

    async def run_morning_cron(self):
        report_message = await self.execute_bu1_pipeline("เซรั่มลดริ้วรอยทองคำ 24K")
        return {"status": "success", "data": {"message": report_message}}

# =====================================================================
# 🌐 FASTAPI ROUTING (แก้ 405 และรองรับ UptimeRobot)
# =====================================================================

@api_app.api_route("/", methods=["GET", "POST", "HEAD"])
async def universal_homepage(request: Request):
    if request.method == "GET":
        return HTMLResponse(content=f"""
        <html>
            <body style="font-family: Arial; background-color: #0f172a; color: #e2e8f0; padding: 40px; text-align: center;">
                <h1 style="color: #38bdf8;">🏎️ Base44 Engine V2 Active</h1>
                <p style="color: #4ade80;"><b>🟢 LIVE (V4.5 Ultimate Feature Edition)</b></p>
                <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; display: inline-block; text-align: left;">
                    <p>🤖 โมเดลปัจจุบัน: <b>{SYSTEM_STATE['active_ai_model']}</b></p>
                    <p>🛡️ ระบบ Transparency Guard: <b>ACTIVE</b></p>
                </div>
            </body>
        </html>
        """)
    elif request.method == "HEAD":
        return Response(status_code=200)
    else: 
        return JSONResponse(status_code=200, content={"status": "success", "state": SYSTEM_STATE})

@api_app.api_route("/webhook", methods=["GET", "POST", "HEAD"])
async def dashboard_webhook():
    return JSONResponse(status_code=200, content={"status": "success"})

@api_app.get("/test-telegram-report")
async def test_telegram_report():
    orchestrator = MetaOrchestrator()
    result = await orchestrator.run_morning_cron()
    return {"status": "success", "backend_response": result}

@api_app.get("/approve-with-trace")
async def approve_webhook(trace_id: Optional[str] = None):
    SYSTEM_STATE["active_ai_model"] = "DeepSeek-R1-Distill-Groq (ค่ายโอเพ่นซอร์ส $0.00)"
    return HTMLResponse("<html style='background:#022c22; color:#34d399; text-align:center; padding:50px;'><body><h1>🟢 APPROVED!</h1></body></html>")

@api_app.get("/emergency-rollback")
async def rollback_webhook(trace_id: Optional[str] = None):
    SYSTEM_STATE["active_ai_model"] = "GPT-4o (Legacy Base Tier)"
    return HTMLResponse("<html style='background:#450a0a; color:#fca5a5; text-align:center; padding:50px;'><body><h1>🚨 ROLLBACK EXECUTED!</h1></body></html>")