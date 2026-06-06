# Complete file: growth_marketing_orchestrator.py
import os
import sys
from pathlib import Path

# 🔌 วางระบบเข็มทิศ Path ป้องกันเอเรอร์บน Linux Cloud (Render)
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# 🕵️‍♂️ Import สายสืบไซเบอร์ (Data Hunting Agent) ที่เราสร้างไว้ในเบอร์ 1
from data_hunting_agent import data_hunting_agent

class GrowthMarketingOrchestrator:
    def __init__(self):
        self.orchestrator_name = "BU_Growth_Marketing_Orchestrator"
        print(f"🎯 [{self.orchestrator_name}] แกนหลักการตลาดเซ็ตอัพโครงสร้างพร้อมรบ!")

    def process_marketing_request(self, user_message: str) -> str:
        """
        ฟังก์ชันเดิมสำหรับรองรับคำสั่งแชทแนวการตลาดจาก Telegram
        """
        print(f"📥 [{self.orchestrator_name}] ได้รับคำสั่งแชท: {user_message}")
        
        # คืนค่า Mock ตอบกลับตาม Keyword (คงโครงสร้างเดิมที่รันผ่านฉลุยไว้)
        if "ไอเดีย" in user_message or "แอด" in user_message:
            return "💡 [Growth Marketing] แนะนำให้ทำแคมเปญ Hook กลุ่มเป้าหมายด้วยคอนเทนต์ 'แจกฟรี' เพื่อดึงดูดสายตาในช่วง 3 วินาทีแรกครับ!"
        
        return f"🤖 [{self.orchestrator_name}] รับทราบคำสั่งการตลาดแล้วครับพ้ม พร้อมนำแผนไปปรับใช้ในระบบถัดไป"

    def analyze_scraped_leads(self) -> list:
        """
        🚀 [ฟังก์ชันใหม่] ดึงดีลเด็ดจาก Scraper Agent แล้วนำมาเขียนคำโปรยยิงแอดการตลาดอัตโนมัติ
        """
        # สั่งสายสืบออกไปขูดข้อมูล
        raw_leads = data_hunting_agent.hunt_for_freebies()
        marketing_reports = []
        
        print(f"📈 [{self.orchestrator_name}] กำลังประมวลผลข้อมูลและทำ Copywriting ระดับ Senior...")
        
        for lead in raw_leads:
            # แปลงร่างข้อมูลดิบให้กลายเป็นคำโปรยแอดโฆษณาเชิงรุก (AIDA Framework Mock)
            ad_copy = (
                f"🔥 **[AI Growth Marketing Hook]** 🔥\n\n"
                f"🎯 **พบขุมทรัพย์ดีลเด็ดจาก:** {lead['source']}\n"
                f"📌 **หัวข้อสินค้า/คอร์ส:** {lead['title']}\n"
                f"🔗 **ลิงก์ตรงเข้าสู่พิกัด:** {lead['url']}\n\n"
                f"✍️ *Senior Copywriting แนะนำสำหรับยิงแอด:*\n"
                f"\"ด่วนที่สุดนายท่าน! ของดีมีเวลาจำกัด คัดสรรมาให้พร้อมลุยทันที คลิกรับสิทธิ์ก่อนตกเทรนด์รอบนี้! 🚀\""
            )
            marketing_reports.append(ad_copy)
            
        print(f"✅ [{self.orchestrator_name}] ผลิตไอเดียคำโปรยยิงแอดเสร็จสิ้น ส่งต่อเข้าสู่ระบบแจ้งเตือน")
        return marketing_reports

# 💎 ประกาศอินสแตนซ์พร้อมใช้งานระดับ Global สำหรับให้ไฟล์อื่น (เช่น telegram_bot.py) เรียกใช้
growth_marketing_orchestrator = GrowthMarketingOrchestrator()