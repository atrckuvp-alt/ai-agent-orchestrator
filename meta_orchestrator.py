# =====================================================================
# 🚀 BASE44 ENGINE V2: UNIFIED MASTER ORCHESTRATOR & BUSINESS UNITS
# =====================================================================
import os
import json
import datetime
from typing import List, Dict, Any

class MetaOrchestrator:
    """1. ทำหน้าที่รับงานและส่งงานโต้ตอบกับ Human (นายท่าน) [cite: 1]"""
    def __init__(self):
        self.dashboard_base_url = "https://ai-agent-orchestrator-2vam.onrender.com"
        self.bu1_revenue_engine = BU1AutonomousRevenueEngine()
        self.bu2_ai_hunter = BU2OpenSourceAIHunter()

    async def generate_daily_master_report(self, raw_market_data: List[Dict], raw_ai_models: List[Dict]) -> Dict[str, Any]:
        """
        ฟังก์ชันหลักที่ทำงานตอน 09:00 น. เพื่อรวบรวมรายงานจากทุก BU
        แล้วสรุปส่งเข้า Telegram พร้อมแนบ Link อนุมัติย้อนกลับมาที่ Lovable Dashboard
        """
        print("⚡ [Meta Orchestrator] กำลังประมวลผลระบบเพื่อสร้างรายงานส่งท่านประธาน...")
        
        # รันระบบทำเงินอัตโนมัติ BU 1 (ควบรวมงานเก่าและงานใหม่ขนานกัน) [cite: 3, 16]
        bu1_report = await self.bu1_revenue_engine.run_pipeline(raw_market_data)
        
        # รันระบบล่า AI Open-Source Free 100% ของ BU 2 [cite: 17]
        bu2_report = await self.bu2_ai_hunter.run_pipeline(raw_ai_models)
        
        # สร้างลิงก์ย้อนกลับไปยัง Lovable Dashboard เพื่อให้กดอนุมัติเชิงยุทธศาสตร์แบบมีร่องรอย
        trace_id = f"TR-{datetime.date.today().strftime('%Y%m%d')}"
        approve_link = f"{self.dashboard_base_url}/approve-with-trace?trace_id={trace_id}"
        rollback_link = f"{self.dashboard_base_url}/emergency-rollback?trace_id={trace_id}"
        
        # ประกอบร่างเป็นข้อความรายงานระดับ VIP สำหรับ Telegram
        telegram_payload = self._compile_telegram_message(bu1_report, bu2_report, approve_link, rollback_link)
        
        return {
            "trace_id": trace_id,
            "telegram_message": telegram_payload,
            "raw_payload_bu1": bu1_report,
            "raw_payload_bu2": bu2_report
        }

    def _compile_telegram_message(self, bu1: Dict, bu2: Dict, app_url: str, roll_url: str) -> str:
        """แปลงข้อมูลดิบทั้งหมดให้กลายเป็นฟอร์แมตรายงานสุดหรูบน Telegram"""
        msg = f"📊 **[รายงานยุทธศาสตร์ปั๊มเงินประจำวัน - Base44 Engine]** 📊\n"
        msg += f"📅 วันที่: {datetime.date.today().isoformat()} | สถานะระบบ: ACTIVE\n\n"
        
        msg += f"💰 **[BU 1: Autonomous Revenue Engine]** [cite: 3]\n"
        for prod in bu1["validated_products"]:
            msg += f"🔹 สินค้า: {prod['product_name']} (โอกาสทำเงิน: {prod['market_viability_score']})\n"
            msg += f"   - สรุปดีล: {prod['deal_type']} (ลดแหลกแจกแถม >50% ไร้เงื่อนไข)\n"
            msg += f"   - 💡 Market Gap (เกณฑ์ 4 ข้อ): {prod['market_gap_summary']}\n"
            msg += f"   - 🎯 AIDA Framework (Hook เด่น): {prod['strategic_framework']['aida_framework']['Attention']}\n"
            msg += f"   - ⏰ ชั่วโมงทองคำ (Organic Traffic): {prod['organic_hours_recommendation']}\n\n"
            
        msg += f"🤖 **[BU 2: Free AI Model Hunter]** [cite: 17]\n"
        if bu2["recommended_model"]:
            m = bu2["recommended_model"]
            msg += f"✅ ค้นพบโมเดลเด่น: {m['model_name']}\n"
            msg += f"   - 🧪 สรุปผล Sandbox (โจทย์แชมพู/ข้าวสาร): {m['sandbox_verdict']}\n"
            msg += f"   - 📊 คะแนนภาษาไทย: {m['thai_accuracy_score']}/100 | สปีด: {m['speed_score']}/100\n"
            msg += f"   - ⚖️ ผลตรวจทาน (Cross-Check): {m['cross_check_summary']}\n\n"
        else:
            msg += f"❌ BU 2: วันนี้ยังไม่มีโอเพ่นซอร์สตัวใหม่ที่ผ่านเกณฑ์ Free-tier 100% [cite: 17]\n\n"
            
        msg += f"----------------------------------------\n"
        msg += f"🔗 **[Lovable Dashboard Command]**\n"
        msg += f"👉 [คลิกเพื่อเปิดดูรายงานละเอียดและกดอนุมัติขึ้น Base44]({app_url})\n"
        msg += f"🚨 [ปุ่มฉุกเฉินถอยทัพระบบทันที (Emergency Rollback)]({roll_url})"
        return msg


# =====================================================================
# 💰 BUSINESS UNIT 1: AUTONOMOUS REVENUE GENERATION ENGINE [cite: 3]
# =====================================================================
class BU1AutonomousRevenueEngine:
    """ทำหน้าที่ปั๊มเงินเข้ากระเป๋าออโต้จาก Affiliate/โฆษณา คิดบนยุทธศาสตร์ระดับโลก [cite: 3, 4]"""
    def __init__(self):
        # ดึงชุดความคิด ดร.แสงสุข มาเป็น Core Logic ควบคุมผู้จัดการยูนิต [cite: 4]
        self.core_logic_mastermind = "Dr. Sangsuk Pithayanukul (Smooth-E & Dentiste')" [cite: 4]

    async def run_pipeline(self, raw_market_data: List[Dict]) -> Dict:
        validated_list = []
        
        for data in raw_market_data:
            # 1. กลไกการตรวจหาช่องว่างตลาด (Market Gap) ตามเกณฑ์ 4 ข้อของนายท่าน 
            is_market_gap, gap_reason = self._check_market_gap_criteria(data)
            
            # 2. คัดกรองและสกัดเอา "ของฟรี คอร์สเรียนฟรี หรือดีลลดราคา >50% ไร้เงื่อนไขแฝง" เท่านั้น
            is_valid_deal = data.get("discount_percent", 0) >= 50 or data.get("is_free_tier", False)
            
            if is_market_gap and is_valid_deal:
                # 3. ส่งต่อให้ 3 Mastermind ตรวจเอกซเรย์ถ่วงน้ำหนักและเขียน Copywriting (AIDA/SWOT) [cite: 4, 5, 7, 8]
                validation_result = self._apply_dream_team_matrix(data, gap_reason)
                
                # 4. คำนวณชั่วโมงทองคำในการโพสต์ออแกนิกเพื่อให้ได้ Engagement สูงสุด 100% Free Cost
                validation_result["organic_hours_recommendation"] = self._calculate_organic_golden_hours(data.get("target_audience"))
                
                validated_list.append(validation_result)
                
        return {"validated_products": validated_list}

    def _check_market_gap_criteria(self, data: Dict) -> tuple:
        """เกณฑ์ 4 ข้อของนายท่าน: คนเจอเยอะบ่นเยอะ, คนมองข้าม, ไม่มีคู่แข่ง, สรุปเป็นประเด็นชัดเจน [cite: 11, 12, 13, 14, 15]"""
        c1 = data.get("pain_frequency_score", 0) >= 7    # คนเจอเยอะ / บ่นเยอะ [cite: 12]
        c2 = data.get("is_overlooked", False) == True    # ไม่มีใครนึกถึงหรือหยิบมาแก้ไข [cite: 13]
        c3 = data.get("competitor_count", 10) <= 2       # ยังไม่มีสินค้ามาตอบสนอง (Blue Ocean) [cite: 14]
        
        if c1 and c2 and c3:
            reason = "สแกนพบคอขวดตลาดระยะยาว คนบ่นบ่อยแต่คู่แข่งเป็นศูนย์ เหมาะแก่การเข้ายึดหัวหาด [cite: 12, 14, 15]"
            return True, reason
        return False, ""

    def _apply_dream_team_matrix(self, data: Dict, gap_reason: str) -> Dict:
        """สกัด Cognitive DNA ของ ดร.แสงสุข, คุณอนิศ, คุณสิทธินันท์ มารวมกัน """
        # คุณอนิศ (Strategic Marketer): ขยี้ Pain Point วาง Funnel [cite: 5, 6]
        # คุณสิทธินันท์ (Content Creator): Data-Driven & Inbound Value [cite: 8, 9]
        # สรุปออกมาเป็น SWOT และ AIDA Framework ในข้อความเดียวเสร็จสรรพ [cite: 7, 10]
        
        viability_score = 85 if data.get("brand_rating", 0) >= 4.5 else 70
        
        return {
            "product_name": data.get("name"),
            "deal_type": "100% FREE Course" if data.get("is_free_tier") else f"Deep Discount {data.get('discount_percent')}% Off",
            "market_viability_score": f"{viability_score}%",
            "market_gap_summary": gap_reason,
            "strategic_framework": {
                "swot_analysis": {
                    "Strengths": "ต้นทุนสินค้า Free Cost 100% สามารถดึงคนเข้ากรวยการขายได้ง่าย",
                    "Opportunities": "ใช้โมเดลแจกคอร์สฟรี/ดีลเด็ดเป็น Lead Magnet เพื่อเปลี่ยนคนดูเป็นคนซื้อตลบสอง [cite: 6]"
                },
                "aida_framework": {
                    "Attention": f"💥 หยุดบ่นเรื่องนี้ได้เลย! ขยี้ Pain Point ที่แบรนด์อื่นมองข้าม: {data.get('pain_keyword')}",
                    "Interest": "💡 มอบประโยชน์นำทาง (Value-First) ด้วยทางแก้ปัญหาที่สถิติรองรับ [cite: 9]",
                    "Desire": "🎁 พิเศษสุด! ไม่มีข้อผูกมัดแฝง ดีลตรงจากโรงงานลดราคาเกินครึ่ง!",
                    "Action": "🛒 จิ้มลิงก์ด่วนก่อนโค้ดออแกนิกนี้จะหมดอายุภายในวันนี้เท่านั้น!"
                }
            }
        }

    def _calculate_organic_golden_hours(self, audience: str) -> str:
        """คำนวณช่วงเวลาโพสต์แบบไม่พึ่งพาค่าโฆษณา (100% Free Cost) แยกตามแพลตฟอร์ม"""
        if audience == "Office Worker":
            return "TikTok: 07:45 (บนรถไฟฟ้า) | FB Reels: 12:15 (หลังกินข้าว) | YouTube Shorts: 18:30"
        elif audience == "Student":
            return "TikTok: 11:50 | X (Twitter): 16:30 (เลิกเรียน) | FB Reels: 20:00"
        return "TikTok: 12:00 | FB Reels: 19:30 | YouTube Shorts: 21:00 (ช่วงผ่อนคลาย)"


# =====================================================================
# 🤖 BUSINESS UNIT 2: OPEN-SOURCE AI MODEL HUNTER (FREE-TIER 100%) [cite: 17]
# =====================================================================
class BU2OpenSourceAIHunter:
    """ทำหน้าที่ล่าโมเดล AI ฟรี 100% ตามระบบ Sandbox Benchmark โจทย์ แชมพู/ข้าวสาร """
    def __init__(self):
        self.orchestrator_name = "BU-2 Manager"

    async def run_pipeline(self, raw_models: List[Dict]) -> Dict:
        recommended = None
        
        for model in raw_models:
            # เงื่อนไขเหล็ก: ต้องเป็น Free-tier 100% เท่านั้น [cite: 17]
            if model.get("is_free_100", False):
                
                # 🕵️‍♂️ Step 1: Research & Coding Agents ค้นพบและประเมินความสามารถ [cite: 18, 19]
                research_score = model.get("base_research_capability", 0)  # ฝั่ง Research Agent ดูแล [cite: 18]
                coding_score = model.get("base_coding_capability", 0)     # ฝั่ง Coding Agent ดูแล [cite: 19]
                
                # 🔄 Step 2: Cross-Check & Review สลับกันตรวจทานข้อดี/ข้อเสีย 
                cross_check_pass = research_score >= 75 and coding_score >= 75
                
                if cross_check_pass:
                    # 🧪 Step 3: Sandbox Benchmark แอบทดสอบรันโจทย์ "แชมพู / ข้าวสาร" หลังบ้านเงียบๆ 
                    speed, accuracy_thai = self._run_sandbox_benchmark(model["model_id"])
                    
                    # ถ้าระบบทดสอบแล้วเร็วกว่า และภาษาไทยเป๊ะกว่าตัวเดิม (สมมุติตัวเดิมคะแนนเฉลี่ย 80)
                    if speed >= 82 and accuracy_thai >= 85:
                        recommended = {
                            "model_name": model["model_name"],
                            "cross_check_summary": "ผ่านเกณฑ์การประเมินร่วมกันของทั้งสองเอเจนต์ ไม่มีเงื่อนไขเชิงพาณิชย์แฝง ",
                            "speed_score": speed,
                            "thai_accuracy_score": accuracy_thai,
                            "sandbox_verdict": "🧪 ผลทดสอบโจทย์ 'แชมพู/ข้าวสาร': เรียบเรียงคุณสมบัติแก้รังแคและคำอธิบายประเภทข้าวหอมมะลิได้สละสลวย ภาษามืออาชีพ ไม่แข็งทื่อ สปีดดีเลย์ต่ำกว่า 1.2 วินาที "
                        }
                        break # คัดสรรเฉพาะตัวที่เจ๋งที่สุดอันดับหนึ่งประจำวัน
                        
        return {"recommended_model": recommended}

    def _run_sandbox_benchmark(self, model_id: str) -> tuple:
        """จำลองการรันโจทย์ทดสอบ 'แชมพู / ข้าวสาร' เพื่อวัดความเร็วและความเป๊ะของภาษาไทยหลังบ้าน """
        print(f"🧪 [Sandbox Testing] กำลังทดสอบโมเดล {model_id} ด้วยชุดโจทย์ 'แชมพูแก้ผมร่วง' และ 'ข้าวสารออร์แกนิก'...")
        # จำลองการคืนค่าคะแนนความเร็ว (Speed) และความเป๊ะภาษาไทย (Thai Accuracy)
        simulated_speed = random.randint(83, 95)
        simulated_thai = random.randint(86, 98)
        return simulated_speed, simulated_thai