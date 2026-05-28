# AI Agent Research Team MVP v1

ระบบนี้เป็น MVP สำหรับสร้างทีม Agent 1 ทีม เพื่อค้นหา AI open-source / free-tier / free API ที่เหมาะกับงาน coding, analysis, research และ reasoning

## สิ่งที่ระบบทำได้ตอนนี้

- มี Orchestrator Agent แบบ workflow
- มี Agent 1: Coding & Analysis Scout
- มี Agent 2: Research & Reasoning Scout
- มี Cross-check Skill
- มี Final Evaluator
- มี Human Approval Gate
- มี Memory แบบ JSON ที่ไม่ลืมข้าม session
- สร้างรายงาน Markdown อัตโนมัติ
- ยังไม่เปลี่ยน model เอง จนกว่า human approve

## วิธีรันบน Windows แบบง่าย

### 1. แตกไฟล์ ZIP

แตกไฟล์ไปไว้ที่ เช่น:

```text
C:\ai_agent_research_team_mvp_v1
```

### 2. เปิด Command Prompt

เข้าโฟลเดอร์:

```bat
cd C:\ai_agent_research_team_mvp_v1
```

### 3. รัน MVP แบบ Mock Mode

```bat
python 04_scripts\run_orchestrator.py --mock
```

ถ้าสำเร็จ จะเห็น:

```text
MVP run completed.
Report created: ...
Check 00_memory/approval_queue.json for human approval requests.
```

### 4. เปิดรายงาน

ดูไฟล์ใน:

```text
03_reports
```

### 5. ดูรายการรออนุมัติ

เปิดไฟล์:

```text
00_memory\approval_queue.json
```

คัดลอก request_id เช่น:

```text
REQ-20260519210000-coding_analysis
```

### 6. อนุมัติ / ปฏิเสธ / ขอทดสอบก่อน

ตัวอย่างทดสอบก่อน:

```bat
python 04_scripts\human_approval.py --request-id REQ-xxxx-coding_analysis --decision TEST_FIRST
```

ตัวอย่างอนุมัติ:

```bat
python 04_scripts\human_approval.py --request-id REQ-xxxx-coding_analysis --decision APPROVE
```

ตัวอย่างปฏิเสธ:

```bat
python 04_scripts\human_approval.py --request-id REQ-xxxx-coding_analysis --decision REJECT
```

## หมายเหตุสำคัญ

MVP v1 ยังไม่เชื่อม live web/API search อัตโนมัติ เพื่อให้ปลอดภัยและเข้าใจง่ายก่อน

MVP v2 ควรเพิ่ม:
- live search ผ่าน OpenRouter / Hugging Face / Groq
- Supabase memory
- Telegram approval
- dashboard
- weekly scheduled run

## API Key ที่เตรียมไว้สำหรับ v2

ดูไฟล์:

```text
.env.example
```

มีตัวแปร:

```text
OPENROUTER_API_KEY
HF_TOKEN
GROQ_API_KEY
```
