# Complete file: 04_scripts/ai_evolution_orchestrator.py
import os
import sys
import requests
import json

# 🔌 ใช้ทางลัดระบุแผนที่โฟลเดอร์ ดึงโมเดลในกลุ่มมาใช้งานแบบไร้บั๊กตัวเลข
current_dir = os.getenv("PYTHONPATH", os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from shared_knowledge import shared_knowledge

class AIResearchAgent:
    def find_new_free_models(self):
        """ [Research Agent] ค้นหาโมเดลออกใหม่ที่ให้ Free-tier """
        # จำลองการตรวจสอบฐานข้อมูล Open-source (ในอนาคตเชื่อมต่อ RSS Feed หรือ API ข่าว)
        return [
            {"name": "deepseek-v3", "type": "marketing", "desc": "ตัวใหม่ล่าสุดจากจีน ฟรีและตอบแผนธุรกิจได้ฉลาดคุ้มค่า"},
            {"name": "phi-4", "type": "research", "desc": "Small model จาก Microsoft เน้นตรรกะแม่นยำสูง"}
        ]

class AICodingAgent:
    def benchmark_model(self, model_name):
        """ [Coding Agent] ทดสอบรันโค้ด Sandbox เพื่อวัดผลความเป๊ะ """
        # จำลองการทดสอบ Benchmark (Sandbox Test) 
        # ในระบบจริงจะมีการยิง Prompt ทดสอบจริงแล้วแปลงออกมาเป็นคะแนนความเสถียร
        score = 88 if "deepseek" in model_name else 72
        return {"score": score, "status": "Stable" if score > 80 else "Unstable"}

class AIEvolutionOrchestrator:
    def __init__(self):
        self.researcher = AIResearchAgent()
        self.coder = AICodingAgent()

    def run_evolution_check(self):
        """ 🎯 ขบวนการรวบรวมผล Sandbox และทำเรื่องส่งขออนุมัติอัปเกรดโมเดลขึ้นหน้าเว็บ Portal """
        print("🔍 [AI Evolution Hub] เริ่มขบวนการสืบค้นและทดสอบโมเดลฟรีออกใหม่...")
        new_discoveries = self.researcher.find_new_free_models()
        
        for model in new_discoveries:
            test_result = self.coder.benchmark_model(model['name'])
            
            # กฎเหล็กโครงการ: ต้องได้คะแนน Sandbox เกิน 80 ถึงจะส่งการ์ดขออนุมัติจากนายท่าน
            if test_result['score'] >= 80:
                upgrade_request = {
                    "model": model['name'],
                    "reason": model['desc'],
                    "score": test_result['score'],
                    "action": f"แนะนำให้พิจารณานำมาใช้สลับแทนโมเดลเดิมในระบบควบคุมหลัก"
                }
                
                # 🚀 ยิงคำร้องเชื่อมต่อไปที่ไฟล์ shared_knowledge.py เพื่อสร้างการ์ดคำขอขึ้นหน้าเว็บทันที
                shared_knowledge.request_ai_upgrade(upgrade_request)
                print(f"🚨 [AI Evolution Hub] ยิงการ์ดคำขออนุมัติสำหรับโมเดล '{model['name']}' ขึ้นเว็บสำเร็จ!")
                return True
                
        print("✨ [AI Evolution Hub] ตรวจสอบแล้ว โมเดลใหม่อื่นๆ ยังไม่ผ่านเกณฑ์กฎเหล็กในรอบนี้")
        return False

ai_evolution_orchestrator = AIEvolutionOrchestrator()