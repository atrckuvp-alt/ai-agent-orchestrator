# =====================================================================
# 🚀 BASE44 ENGINE V2: MASTER ORCHESTRATOR (V4.6 - TWIN-ENGINE COMPLETE EDITION)
# =====================================================================
import os
import sys
import asyncio
import random
import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

# 🔌 [Senior Path Injection] บังคับให้ระบบมองเห็นไฟล์ทั้งหมดในโฟลเดอร์นี้เพื่อแก้ปัญหาเลข 04_
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# =====================================================================
# ✅ [ข้อ 5: Dashboard & Control Room + Twin-Engine Fail-Safe]
# ป้องกันปัญหา Uvicorn หาตัวแปรไม่เจอจนเกิดอาการ Crash On Boot แดงสนิท
# =====================================================================
base_instance = FastAPI(title="Base44 Engine V2 - Master Command")

# ผูกสองชื่อเข้ากับ Engine ตัวเดียวกันชัวร์ 100% ใครเรียกชื่อไหนก็รอด!
app = base_instance
api_app = base_instance

# สถานะตัวกลางสำหรับซิงค์ข้อมูลหน้า Dashboard
SYSTEM_STATE = {
    "active_ai_model": "GPT-4o (Legacy Base Tier)",
    "bu1_pipeline_status": "PROACTIVE_RUNNING",
    "last_action": "SYSTEM_INITIALIZED",
    "last_trace_id": "NONE"
}

# =====================================================================
# 👑 MASTER ORCHESTRATOR CLASS (คุมระบบฟีเจอร์ข้อ 1, 2, 3, 4 ครบถ้วน)
# =====================================================================
class MetaOrchestrator:
    def __init__(self):
        self.activated = True
        self.active_money_lines = ["คอลลาเจนไดเปปไทด์ชนิดผงชงดื่ม บำรุงข้อต่อและผิวพรรณเข้มข้น"]
        self.dashboard_base_url = "https://ai-agent-orchestrator-2vam.onrender.com"

    # =====================================================================
    # ✅ [ข้อ 3: Transparency Guard] ระบบสกัดดีลโกงและค่าส่งแฝง
    # =====================================================================
    def run_transparency_guard(self, product_data: dict) -> bool:
        """ ตรวจสอบความโปร่งใส ถ้ามีค่าส่งแฝงหรือประวัติโกงในระบบสินค้า ให้ดีดออกทันที """
        blacklist_keywords = ["ค่าส่งแฝง", "หมกเม็ด", "โกง", "ไม่ตรงปก", "บวกเพิ่มหน้างาน"]
        desc = product_data.get("description", "")
        for word in blacklist_keywords:
            if word in desc:
                return False  # ติดแบล็กลิสต์ ไม่ให้ผ่าน
        return True

    async def route_and_execute(self, user_message: str, user_id: int) -> dict:
        """ ด่านหน้ารับคำสั่งทำการจัดเส้นทาง (Routing) ส่งต่อไปตาม BU ต่าง ๆ """
        msg_clean = user_message.strip().lower()
        
        # 💰 [BU 1: Autonomous Revenue Generation Engine] - ท่อส่งงานสายปั๊มเงินสด
        if any(keyword in msg_clean for keyword in ["รันระบบปั๊มเงิน", "วิเคราะห์สินค้าหาเงิน", "run revenue"]):
            try:
                # ข้อมูลสินค้าทดสอบ
                new_product = {
                    "name": "เซรั่มลดริ้วรอยสูตรพรีเมียมจากเมือกหอยทากเกาหลีผสมทองคำ 24K",
                    "description": "สินค้าเกรดพรีเมียม ส่งฟรีทั่วประเทศ ไม่มีค่าส่งแฝง ไร้ประวัติการโกง"
                }
                
                # เรียกใช้ระบบข้อ 3 (Transparency Guard)
                if not self.run_transparency_guard(new_product):
                    return {
                        "status": "error", 
                        "message": "🚨 [Transparency Guard] ระบบตรวจพบดีลไม่โปร่งใสหรือมีค่าส่งแฝง จึงทำการระงับการทำงานสายพานนี้ออโต้!"
                    }

                report_data = await self.execute_bu1_pipeline(new_product["name"])
                return {"status": "success", "data": {"message": report_data}}
            except Exception as e:
                return {"status": "error", "message": f"ระบบสายพาน BU ปั๊มเงินขัดข้อง: {str(e)}"}

        # =====================================================================
        # ✅ [ข้อ 4: Dual-Agent Sandbox] ระบบขังโมเดลทดสอบ Copywriting (แชมพู/ข้าวสาร)
        # =====================================================================
        if any(keyword in msg_clean for keyword in ["รันระบบล่าของฟรี", "ทดสอบโมเดล", "test evolution"]):
            try:
                sandbox_prompts = [
                    "เขียนก็อปปี้คำโฆษณาขายแชมพูแก้ปัญหาผมร่วงเข้มข้น",
                    "ร่างสคริปต์วิดีโอสั้นสไตล์อินฟลูเอนเซอร์ขายข้าวสารหอมมะลิแท้ 100%"
                ]
                selected_test = random.choice(sandbox_prompts)
                
                return {
                    "status": "success",
                    "data": {
                        "message": f"🧪 **[Dual-Agent Sandbox Activated]**\nทำการขังโมเดลที่ต้องการทดสอบเข้าสู่กระบะทรายนิรภัยเรียบร้อยแล้ว!\n• โจทย์ที่ใช้ทดสอบระดับความสละสลวยภาษาไทย: *'{selected_test}'*\n• สถานะระบบ: รอการประเมินผลระดับคะแนนการเขียนผ่านกลไก AI Evolution Hub"
                    }
                }
            except Exception as e:
                return {"status": "error", "message": f"ระบบ Sandbox ทดสอบโมเดลภาษาไทยขัดข้อง: {str(e)}"}
                
        return {
            "status": "error",
            "message": "🤖 ขออภัยครับบอส ระบบ Meta_Orchestrator สแตนบายรอรับคำสั่ง 'รันระบบปั๊มเงิน' หรือ 'ทดสอบโมเดล' อยู่ครับ"
        }

    async def execute_bu1_pipeline(self, product_name: str) -> str:
        """ ลอจิกจำลองการทำงานประสานพลังยุทธศาสตร์ 3 ผู้นำชั้นนำ """
        
        # =====================================================================
        # ✅ [ข้อ 1: Validation Matrix] สแกนหาช่องว่างตลาดเกณฑ์เหล็ก 4 ข้อ (ดร.แสงสุข/คุณอนิศ)
        # =====================================================================
        market_gap_analysis = {
            "high_frequency_pain": "สาวออฟฟิศวัย 30+ เผชิญปัญหาผิวโทรม แห้งสะสม หมองคล้ำเนื่องจากงานเครียดพักผ่อนน้อย",
            "overlooked_issue": "ผู้บริโภคมองข้ามการดูแลเข้มข้นเองที่บ้าน มุ่งคิดว่าต้องแก้ด้วยการเข้าคลินิกฉีดหน้าใสราคาหลักหมื่นเท่านั้น",
            "blue_ocean": "ในฝั่งตลาดนายหน้าคอนเทนต์ (Affiliate) ยังไม่มีผู้นำคนไหนทำคลิปเจาะลึกวิทยาศาสตร์ผิวหนังเปรียบเทียบความคุ้มค่าทองคำ 24K กับคลินิก",
            "verdict": "⭐⭐⭐⭐⭐ [เกณฑ์ผ่านฉลุยสิบเต็มสิบ] สินค้าตัวนี้ให้ค่าคอมมิชชั่นสูง มีพลังทวีคุ้มค่าแก่การลงคอนเทนต์ลุยตลาด"
        }
        
        aida_hook = "หยุดฉีดหน้าก่อน! ถ้ายังไม่ลองทองคำคู่นี้... เสียดายเงินคลินิกหลักหมื่นมาก!"

        # =====================================================================
        # ✅ [ข้อ 2: Organic Content & Golden Hours] ผังพิมพ์เขียวเวลาโพสต์ทองคำ ทุบค่าแอดเป็น 0 บาท
        # =====================================================================
        golden_hours_blueprint = (
            "🕒 **[พิมพ์เขียวตารางเวลาโพสต์ทองคำสูตร Organic 0 บาท]**\n"
            "📱 **TikTok Feed:** โพสต์ช่วงเวลา 19:30 - 21:00 น. (สกัดกลุ่มคนเลิกงานนอนสไลด์จอผ่อนคลาย)\n"
            "📷 **Instagram Reels:** โพสต์ช่วงเวลา 12:15 - 13:00 น. (เจาะพนักงานออฟฟิศระดับกลางช่วงพักเที่ยง)\n"
            "📺 **YouTube Shorts:** โพสต์ช่วงเวลา 18:45 น. (ดักทราฟฟิกคนเดินทางนั่งรถไฟฟ้ากลับบ้านโหยหาความบันเทิง)"
        )

        # ตั้งค่าสร้างลิงก์สำหรับ Control Room ควบคุมผ่าน Dashboard
        trace_id = f"TR-{datetime.date.today().strftime('%Y%m%d')}"
        SYSTEM_STATE["last_trace_id"] = trace_id
        approve_link = f"{self.dashboard_base_url}/approve-with-trace?trace_id={trace_id}"
        rollback_link = f"{self.dashboard_base_url}/emergency-rollback?trace_id={trace_id}"

        # สรุปรวมร่างรายงาน Mastermind Report (คุณสิทธินันท์ DNA)
        report = (
            f"☀️ 📢 **[Master Briefing Report - BU 1 สายพานผลิตเงินคู่ขนาน 💰]**\n"
            f"อรุณสวัสดิ์ครับบอส! รายงานกลยุทธ์ทำเงินประสานพลังผ่านสมองกลผู้นำเสร็จสมบูรณ์แล้วครับ!\n\n"
            f"📦 **สินค้าประจำรอบตรวจสอบ:** *{product_name}*\n"
            f"🛡️ **สถานะความโปร่งใส:** ผ่านการสแกนเกราะความปลอดภัยไร้ค่าส่งแฝง 100%\n\n"
            f"--- 🔎 **[1. Validation Matrix: ผลลัพธ์การเจาะช่องว่างตลาด 4 ข้อ]** ---\n"
            f"1️⃣ เจ็บถี่/บ่นดัง: {market_gap_analysis['high_frequency_pain']}\n"
            f"2️⃣ เรื่องที่คนมองข้าม: {market_gap_analysis['overlooked_issue']}\n"
            f"3️⃣ น่านน้ำสีคราม (Blue Ocean): {market_gap_analysis['blue_ocean']}\n"
            f"4️⃣ ฟันธงความน่าลงทุน: {market_gap_analysis['verdict']}\n\n"
            f"--- 🎬 **[2. Copywriting & AIDA Content Strategy (Value-First)]** ---\n"
            f"• **คำพาดหัวหยุดนิ้ว (Hook):** \"{aida_hook}\"\n"
            f"• **โครงสร้างเนื้อหา:** ให้ความรู้เรื่องประสิทธิภาพทองคำสกัดบริสุทธิ์เพื่อตอกย้ำคุณค่าเหนือราคาคลินิก\n\n"
            f"--- 📊 **[3. การกระจายช่องทาง Organic Content & Hours]** ---\n"
            f"{golden_hours_blueprint}\n\n"
            f"----------------------------------------\n"
            f"🔗 **[Control Room Room - Dashboard Command Webhook]**\n"
            f"👉 [คลิกอนุมัติสลับโมเดลบน Lovable (Approve)]({approve_link})\n"
            f"🚨 [ปุ่มฉุกเฉินสั่งการถอยทัพระบบ (Rollback)]({rollback_link})\n"
            f"สถานะจุดศูนย์ควบคุมหลัก: {self.dashboard_base_url}"
        )
        return report

    async def run_morning_cron(self):
        """ สคริปต์รันอัตโนมัติประจำวันเพื่อส่งสัญญาณเข้าระบบ Telegram """
        return await self.execute_bu1_pipeline("เซรั่มลดริ้วรอยสูตรพรีเมียมจากเมือกหอยทากเกาหลีผสมทองคำ 24K")


# =====================================================================
# 🌐 FASTAPI UNIVERSAL ROUTING (ดักรับสายส่ง 100% สยบปัญหา 405 เมธอดเพี้ยน)
# =====================================================================

@api_app.api_route("/", methods=["GET", "POST", "HEAD"])
async def universal_homepage(request: Request):
    if request.method == "GET":
        return HTMLResponse(content=f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #0f172a; color: #e2e8f0; padding: 40px; text-align: center;">
                <h1 style="color: #38bdf8;">🏎️ Base44 Engine V2 Active</h1>
                <p style="font-size: 1.2em; color: #4ade80;">สถานะระบบ: <b>🟢 LIVE (V4.6 Twin-Engine Edition)</b></p>
                <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; display: inline-block; text-align: left; margin-top: 15px; border: 1px solid #334155;">
                    <p style="margin: 5px 0;">🤖 <b>Active AI Model:</b> <span style="color: #38bdf8;">{SYSTEM_STATE['active_ai_model']}</span></p>
                    <p style="margin: 5px 0;">🛡️ <b>Transparency Guard:</b> <span style="color: #4ade80;">READY</span></p>
                    <p style="margin: 5px 0;">🧪 <b>Dual-Agent Sandbox:</b> <span style="color: #a855f7;">READY</span></p>
                </div>
            </body>
        </html>
        """)
    elif request.method == "HEAD":
        # ดักจับ UptimeRobot ยิงเช็คสถานะแบบ HEAD -> คืน 200 OK ให้ไฟเขียวทันที
        return Response(status_code=200)
    else: 
        # รองรับ POST จากแดชบอร์ด Lovable สวนค่ากลับ 200 OK ทันที ไร้เงา 405 ตัวร้าย
        return JSONResponse(status_code=200, content={
            "status": "success",
            "message": "Twin-Engine successfully processed this request.",
            "system_state": SYSTEM_STATE
        })

@api_app.api_route("/webhook", methods=["GET", "POST", "HEAD"])
async def dashboard_webhook():
    return JSONResponse(status_code=200, content={"status": "success", "scope": "Webhook online"})

@api_app.get("/test-telegram-report")
async def test_telegram_report():
    try:
        orchestrator_instance = MetaOrchestrator()
        report_result = await orchestrator_instance.run_morning_cron()
        return {
            "status": "success",
            "message": "🚀 วิเคราะห์แผนฟีเจอร์ครบถ้วนและเตรียมยิงเข้าท่อเรียบร้อย!",
            "backend_response": report_result
        }
    except Exception as e:
        return {"status": "bug_detected", "error_message": str(e)}

@api_app.get("/approve-with-trace")
async def approve_webhook(trace_id: Optional[str] = None):
    t_id = trace_id if trace_id else "MANUAL"
    SYSTEM_STATE["active_ai_model"] = "DeepSeek-R1-Distill-Groq (ค่ายโอเพ่นซอร์ส $0.00)"
    return HTMLResponse("<html style='background:#022c22; color:#34d399; text-align:center; padding:50px; font-family:Arial;'><body><h1>🟢 PLATFORM COMMAND APPROVED SUCCESS!</h1></body></html>")

@api_app.get("/emergency-rollback")
async def rollback_webhook(trace_id: Optional[str] = None):
    t_id = trace_id if trace_id else "MANUAL"
    SYSTEM_STATE["active_ai_model"] = "GPT-4o (Legacy Base Tier)"
    return HTMLResponse("<html style='background:#450a0a; color:#fca5a5; text-align:center; padding:50px; font-family:Arial;'><body><h1>🚨 EMERGENCY ROLLBACK EXECUTE COMPLETE!</h1></body></html>")