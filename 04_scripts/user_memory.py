import json
from pathlib import Path
import datetime as dt
from memory_manager import memory_manager

class UserMemory:
    def __init__(self):
        pass

    def get_context(self, user_id: int) -> dict:
        """แปลงรูปแบบจาก Long-term Memory เพื่อส่งต่อไปยัง Intent Router และ Orchestrator"""
        full_mem = memory_manager.load_memory(user_id)
        lt = full_mem.get("long_term_summary", {})
        
        # เชื่อมโยงบริบททางธุรกิจและข้อแนะนำเรื่องต้นทุนส่งกลับไปเสริมปัญญาให้ระบบสั่งการ
        summary_context = f"Business Objective: {lt.get('business_context', 'None')}. Recommendation & Cloud Cost Log: {', '.join(lt.get('cost_optimization_logs', []))}"
        
        return {
            "current_intent": "general",
            "summary_context": summary_context,
            "extracted_entities": {
                "teams": lt.get("teams_discovered", []),
                "workflows": lt.get("workflows_used", []),
                "open_source": lt.get("discovered_open_source", []),
                "keywords": lt.get("essential_keywords", [])
            }
        }

    def update_context(self, user_id: int, summary_context: str, current_intent: str, entities: dict = None):
        """รับการอัปเดตค่าจากภายนอก แล้วผสานคืนลงสู่หน่วยความจำระยะยาวศูนย์กลาง"""
        full_mem = memory_manager.load_memory(user_id)
        lt = full_mem["long_term_summary"]
        
        if summary_context and len(summary_context.strip()) > 0:
            lt["business_context"] = summary_context

        if entities:
            # ค่อยๆ ผสานค่าอาร์เรย์เอนทิตีโดยใช้ set เพื่อป้องกันคีย์เวิร์ดและเครื่องมือซ้ำซ้อนกัน
            if "teams" in entities and isinstance(entities["teams"], list):
                lt["teams_discovered"] = list(set(lt["teams_discovered"] + entities["teams"]))
            if "workflows" in entities and isinstance(entities["workflows"], list):
                lt["workflows_used"] = list(set(lt["workflows_used"] + entities["workflows"]))
            if "open_source" in entities and isinstance(entities["open_source"], list):
                lt["discovered_open_source"] = list(set(lt["discovered_open_source"] + entities["open_source"]))
            if "keywords" in entities and isinstance(entities["keywords"], list):
                lt["essential_keywords"] = list(set(lt["essential_keywords"] + entities["keywords"]))

        lt["last_updated"] = dt.datetime.now().isoformat()
        memory_manager.save_memory(user_id, full_mem)

user_memory = UserMemory()