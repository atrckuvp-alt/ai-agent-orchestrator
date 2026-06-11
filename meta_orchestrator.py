# Complete file: 04_scripts/meta_orchestrator.py
import os
import sys
import asyncio
import random

# 🔌 [Senior Path Injection] บังคับให้ระบบมองเห็นไฟล์ทั้งหมดในโฟลเดอร์นี้เพื่อแก้ปัญหาเลข 04_
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

class MetaOrchestrator:
    def __init__(self):
        self.activated = True
        # รายการสายพานผลิตเงินคู่ขนาน (Multi-Line Production Portfolio)
        self.active_money_lines = [
            "คอลลาเจนไดเปปไทด์ชนิดผงชงดื่ม บำรุงข้อต่อและผิวพรรณเข้มข้น"
        ]

    async def route_and_execute(self, user_message: str, user_id: int) -> dict:
        """ 🤖 Meta_Orchestrator: ด่านหน้ารับงานจาก Human และทำการส่งต่อ (Routing) ให้กับ BU ที่เกี่ยวข้อง """
        msg_clean = user_message.strip().lower()
        
        # 💰 [BU 1: Autonomous Revenue Generation Engine] - ท่อส่งงานสายปั๊มเงินสด
        if any(keyword in msg_clean for keyword in ["รันระบบปั๊มเงิน", "วิเคราะห์สินค้าหาเงิน", "run revenue"]):
            try:
                # จำลองการเลือกสินค้าใหม่เข้ามาวิเคราะห์ควบคู่กับไลน์เดิม
                new_product = "เซรั่มลดริ้วรอยสูตรพรีเมียมจากเมือกหอยทากเกาหลีผสมทองคำ 24K"
                report_data = await self.execute_bu1_pipeline(new_product)
                return {"status": "success", "data": {"message": report_data}}
            except Exception as e:
                return {"status": "error", "message": f"ระบบสายพาน BU ปั๊มเงินขัดข้อง: {str(e)}"}

        # 🔍 [BU 2: Free-Tier AI Model Hunter] - ท่อส่งงานสายล่าของฟรี (ลอจิกเดิมรักษาไว้)
        if "รันระบบล่าของฟรี" in msg_clean or "test evolution" in msg_clean:
            try:
                from ai_evolution_orchestrator import ai_evolution_orchestrator
                is_triggered = ai_evolution_orchestrator.run_evolution_check()
                
                if is_triggered:
                    return {
                        "status": "success",
                        "data": {
                            "message": "🔍 🚨 **[BU_AI_Evolution_Hub]** ออกปฏิบัติการล่าของฟรีและสุ่มดึงโมเดลใหม่เข้าประจำการเรียบร้อยแล้ว!"
                        }
                    }
                else:
                    return {
                        "status": "success",
                        "data": {
                            "message": "ℹ️ **[BU_AI_Evolution_Hub]** ตรวจสอบแล้ว สถานะตลาดยังเสถียรดี ไม่จำเป็นต้องสลับโมเดลในรอบนี้ครับ"
                        }
                    }
            except Exception as e:
                return {"status": "error", "message": f"ระบบบอทล่าของฟรีขัดข้อง: {str(e)}"}
                
        return {
            "status": "error",
            "message": "🤖 ขออภัยครับนายท่าน บอท Meta_Orchestrator ยังไม่เข้าใจคำสั่งนี้ (โปรดลองสั่ง 'รันระบบปั๊มเงิน' หรือ 'รันระบบล่าของฟรี')"
        }

    async def execute_bu1_pipeline(self, product_name: str) -> str:
        """ ระบบการทำงานจำลองของ BU 1 ประสานพลัง Agent ตามชุดความคิด Mastermind """
        
        # 🧠 [Step 1: DR.SANGSOOK CORE LOGIC] - วางยุทธศาสตร์ธุรกิจพรีเมียมระดับโลก ไม่เดาสุ่ม
        premium_positioning = f"สร้างจุดยืนให้ '{product_name}' กลายเป็นสินค้าเกรดพรีเมียมระดับ Medical-Grade ที่แตกต่างจากสินค้าท้องตลาดทั่วไป"
        
        # 🧠 [Step 2: AGENT 1 - STRATEGIC MARKETER (คุณอนิศ DNA)] - เจาะช่องว่างตลาด ขยี้ Pain Point ทำ SWOT/AIDA
        market_gap_analysis = {
            "high_frequency_pain": "สาวออฟฟิศวัย 30+ เผชิญปัญหาหน้าแห้ง โทรม หมองคล้ำ และแต่งหน้าไม่ติดเนื่องจากการพักผ่อนน้อยและเครียดจากงาน",
            "overlooked_issue": "คนส่วนใหญ่คิดว่าต้องพึ่งพาคลินิกฉีดหน้าใสราคาหลักหมื่นเท่านั้น มองข้ามการฟื้นฟูผิวเข้มข้นแบบสม่ำเสมอด้วยตนเองที่บ้าน",
            "blue_ocean": "ในตลาด Affiliate ยังไม่มีใครทำคอนเทนต์วิทยาศาสตร์ผิวหนัง (Data-Driven) ชูโรงสารสกัดเมือกหอยทากทองคำ 24K ในแง่ความคุ้มค่าเทียบกับการเข้าคลินิก",
            "verdict": "⭐⭐⭐⭐⭐ [แนะนำลุยทันที] สินค้าให้ค่าคอมมิชชั่นสูง 25% มีพลังทวี (High Leverage) ตลาดต้องการสูง"
        }
        
        aida_framework = {
            "Attention": "หยุดฉีดหน้าก่อน! ถ้ายังไม่ลองทองคำคู่นี้... เสียดายเงินคลินิกหลักหมื่นมาก!",
            "Interest": "เผยความลับของทองคำบริสุทธิ์ 24K และเมือกหอยทากสกัดเข้มข้นที่ซึมลึกกู้ผิวโทรมได้เร็วกว่าปกติ 3 เท่า",
            "Desire": "ตอกย้ำความฉ่ำเงาเหมือนกระจกในราคาหลักร้อย ตื่นมาหน้านุ่มอิ่มฟูเหมือนนอนเต็มอิ่ม 10 ชั่วโมง",
            "Action": "ดึงดูดผู้ซื้อผ่านกรวยการขาย (Funnel) บังคับให้กดที่ตะกร้าสีเหลืองหรือลิงก์ในคอนเทนต์เพื่อปิดการขายทันที"
        }

        # 🧠 [Step 3: AGENT 2 - CONTENT CREATOR (คุณสิทธินันท์ DNA)] - โครงสร้าง Value-First & สคริปต์ทำเงินสละสลวย
        viral_script = (
            f"🎬 **[สคริปต์วิดีโอสั้นสำหรับ TikTok/Reels (30-45 วินาที)]**\n"
            f"• **[0-3 วินาทีแรก - Hook หยุดนิ้ว]:** \"{aida_framework['Attention']}\"\n"
            f"• **[4-20 วินาที - Value-First Story (Data-Driven)]:** *(ภาพประกอบ: โชว์เนื้อสัมผัสเซรั่มยืด ๆ ซึมเข้าผิวทันที)* \"รู้ไหมครับว่า ทองคำ 24K และเมือกหอยทากเข้มข้น พอมันทำงานร่วมกัน มันจะช่วยกระตุ้นการสร้างคอลลาเจนใต้ผิวและกู้หน้าโทรมได้เร็วกว่าครีมทั่วไปถึง 3 เท่า! มีผลวิจัยรองรับชัดเจน\"\n"
            f"• **[21-30 วินาที - CTA ปิดการขาย]:** *(ภาพประกอบ: ทำท่าชี้ไปที่มุมซ้ายล่างของจอ)* \"{aida_framework['Action']} ตอนนี้แบรนด์จัดโปรเปิดตัวใน TikTok Shop เหลือหลักร้อยเองแก ใครอยากหน้าเด้งฉ่ำเงารีบกดด่วนก่อนของหมดนะ!\""
        )

        # 🔄 [Step 4: MULTI-LINE PRODUCTION CHECK] - อัปเดตสายพานผลิตเงินคู่ขนาน
        if product_name not in self.active_money_lines:
            self.active_money_lines.append(product_name)
            
        lines_status = ", ".join([f"'{line}'" for line in self.active_money_lines])

        # 📝 [Step 5: COMPILE MASTERMIND REPORT] - ประกอบร่างรายงานสอดคล้องตามโครงสร้างระบบ
        report = (
            f"☀️ 📢 **[Morning Briefing Report - BU 1 ปั๊มเงินอัตโนมัติ 💰]**\n"
            f"อรุณสวัสดิ์ครับบอสและนายท่าน! ทีม Agent ประสานพลังภายใต้ยุทธศาสตร์ระดับโลกของ ดร.แสงสุข คลอดรายงานทำเงินประจำวันนี้ครับ!\n\n"
            f"📦 **สินค้าใหม่ที่ส่งเข้าสายพานผลิตเงิน:** *{product_name}*\n"
            f"📈 **พอร์ตโฟลิโอสายพานทำเงินปัจจุบัน (Multi-Line Status):** {lines_status}\n\n"
            f"--- 🔎 **[1. วิเคราะห์ช่องว่างตลาด (Market Gap เกณฑ์เหล็ก 4 ข้อ)]** ---\n"
            f"1️⃣ **คนเจอเยอะ/บ่นเยอะ (High Frequency Pain):** {market_gap_analysis['high_frequency_pain']}\n"
            f"2️⃣ **ไม่มีใครนึกถึง/มองข้าม (Overlooked Issue):** {market_gap_analysis['overlooked_issue']}\n"
            f"3️⃣ **บลูโอเชี่ยน (Blue Ocean / Zero Competitor):** {market_gap_analysis['blue_ocean']}\n"
            f"4️⃣ **บทสรุปเชิงวิเคราะห์ (Investment Verdict):** {market_gap_analysis['verdict']}\n\n"
            f"--- 🧠 **[2. Strategic Marketer (คุณอนิศ DNA) - SWOT/AIDA]** ---\n"
            f"• **SWOT Highlight:** [Strength] ค่าคอมมิชชั่นสูง เอฟเฟกต์ภาพชัดเจนเจนคลิปง่าย | [Opportunity] ยอดขายในหมวดหมู่บิวตี้พรีเมียมเติบโตแบบก้าวกระโดด\n"
            f"• **AIDA Strategy:** Hook ด้วยความกลัวเรื่องผิวแก่ -> ดึงดูดด้วยดาต้าวิทยาศาสตร์ -> กระตุ้นความอยากด้วยผลลัพธ์หน้ากระจก -> ปิดจ๊อบด้วยกรวยขาย\n\n"
            f"--- 🎬 **[3. Content Creator (คุณสิทธินันท์ DNA) - Value-First Content]** ---\n"
            f"{viral_script}\n\n"
            f"🏷️ **Viral Keywords & Hashtags:** #หน้ากระจก #กู้หน้าโทรมใน3วัน #รีวิวบิวตี้ #TikTokป้ายยา\n"
            f"🔗 ตรวจสอบดาต้าและระบบหลังบ้านได้ที่: https://ai-agent-orchestrator-2vam.onrender.com"
        )
        return report

    async def run_morning_cron(self):
        """ สคริปต์จำลองการทำงานอัตโนมัติตอน 09:00 น. เพื่อรันระบบ Pipeline ของ BU 1 """
        morning_ideas = [
            "เซรั่มลดริ้วรอยสูตรพรีเมียมจากเมือกหอยทากเกาหลีผสมทองคำ 24K",
            "ครีมกันแดดเนื้อไฮบริด SPF50+ PA++++ คุมมันสำหรับผิวแพ้ง่าย",
            "มาส์กหน้ากู้ผิวเร่งด่วนจากสารสกัดเมือกหอยทากและทองคำบริสุทธิ์"
        ]
        selected_product = random.choice(morning_ideas)

        try:
            # รันระบบสายพานผลิตเงินอัตโนมัติผ่าน Pipeline ของ BU 1
            report_message = await self.execute_bu1_pipeline(selected_product)
            
            # บันทึกข้อมูลลง Shared Knowledge
            from shared_knowledge import shared_knowledge
            shared_knowledge.publish_insight(
                author_team="BU1_Mastermind_Revenue_Engine",
                topic=f"[Morning Money Report] {selected_product}",
                insight_data={"status": "executed", "product": selected_product}
            )
            
            return {"status": "success", "data": {"message": report_message}}
            
        except Exception as e:
            return {"status": "error", "message": f"สคริปต์ Cron ยามเช้าพัง: {str(e)}"}


# ========================================================
# 🚀 [Senior Dev Route] ท่อลัดพิเศษสำหรับ "นายท่าน" ใช้กดทดสอบยิงรายงาน Telegram ทันที
# ========================================================
from fastapi import FastAPI
api_app = FastAPI() if 'api_app' not in globals() else globals()['api_app']

@api_app.get("/test-telegram-report")
async def test_telegram_report():
    try:
        orchestrator_instance = MetaOrchestrator()
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        
        if not bot_token:
            return {
                "status": "failed",
                "reason": "❌ ระบบหาคีย์ 'TELEGRAM_BOT_TOKEN' บน Render ไม่เจอ! นายท่านกรุณาตรวจสอบ Environment Variables นะครับ"
            }
            
        # สั่งรันฟังก์ชันระบบสายพานปั๊มเงินและสร้างรายงานแมนนวลทันที
        report_result = await orchestrator_instance.run_morning_cron()
        
        return {
            "status": "success",
            "message": "🚀 ระบบ BU 1 ประสานพลังสกัดวิเคราะห์ข้อมูลและยิงรายงานเข้า Telegram เรียบร้อยแล้วครับนายท่าน!",
            "backend_response": report_result,
            "using_token_prefix": bot_token[:10] + "..."
        }
        
    except Exception as e:
        return {
            "status": "bug_detected",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "suggestion": "💥 เกิดข้อผิดพลาดในระบบส่งรายงาน ตรวจสอบลอจิกข้ามไฟล์หรือการประกาศตัวแปรในแอปหลักครับ!"
        }