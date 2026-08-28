# 👳‍♂️ Starbug AI Assistant (สตาร์บั๊ก ประเทศไทย สาขาภารตะแดนสวรรค์ ☕)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)](https://flask.palletsprojects.com/)
[![LINE Bot SDK](https://img.shields.io/badge/LINE_Bot_SDK-v3-00c300.svg)](https://developers.line.biz/)
[![Sentence Transformers](https://img.shields.io/badge/BERT-MiniLM--L12--v2-orange.svg)](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
[![PyThaiNLP](https://img.shields.io/badge/PyThaiNLP-5.3+-brightgreen.svg)](https://github.com/PyThaiNLP/pythainlp)
[![RapidFuzz](https://img.shields.io/badge/RapidFuzz-3.14+-yellow.svg)](https://github.com/maxbachmann/RapidFuzz)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> [!NOTE]
> 🎓 **Educational Disclaimer:**
> This project is developed strictly for **educational, academic, and non-commercial research purposes** as part of the university coursework (*AI for Social*). All brand assets, product names, images, and menu data belong to their respective copyright holders (Starbucks Corporation / Starbucks Thailand). "Starbug" is a parody and simulation project designed to explore Thai Natural Language Processing (NLP), recommendation algorithms, and conversational UI engineering.

## 📖 English Overview
**Starbug** is an AI-powered conversational assistant built for the LINE Messaging Platform and Web. It simulates an intelligent, entertaining virtual barista featuring a complete 64-item catalog, real-time Neural BERT Thai NLP intent classification, multi-criteria menu filtering, dynamic cup size pricing, interactive 2-step ordering, and LINE Flex Message carousels.

---

## 🌟 จุดเด่นของระบบ (Key Features & Highlights)

1. **👳‍♂️ บาริสต้าสายฮาสไตล์ภารตะ (Indian Chaiwala & Bollywood Banter)**:
   - ต้อนรับผู้ใช้ด้วยรูปบาริสต้าในตำนาน (Dolly Chaiwala) พร้อมคำทักทาย *"ยินดีต้อนรับสู่ Starbug สาขาภารตะแดนสวรรค์นะจ๊ะนายจ๋า!"*
   - ลูกเล่นสุดกวน: บทสนทนาสายฮาภารตะแดนสวรรค์ และมุกแซวคนสั่งกาแฟบาริสต้าปากแซ่บ (🤣)

2. **☕ เมนูสมบูรณ์แบบ 64 รายการ (Comprehensive Catalog with 100% Live Assets)**:
   - รวบรวมเมนูครบทั้ง **เครื่องดื่ม (กาแฟสด, เอสเพรสโซ่, ชาเขียว Teavana, แฟรปปูชิโน่ปั่น, รีเฟรชเชอร์)** และ **เบเกอรี่/ของว่าง (ครัวซองต์, เค้ก, พายแอปเปิ้ล, ฮันนี่โทสต์, เดนิช, ทาร์ต, คุกกี้, เบเกิล)**
   - รองรับเมนูใหม่ล่าสุด **New Arrivals** (เช่น คาราเมลพุดดิ้งแฟรปปูชิโน่, ที-รามิสุครีม, ยูสุแอโร่กาโน่)
   - ภาพประกอบความละเอียดสูงจาก CDN ทางการของ Starbucks Thailand แคชพร้อมเสิร์ฟครบทุกเมนู 100%

3. **🧠 Neural Multilingual BERT & 4-Tier Hybrid NLP Engine**:
   - **Deep Transformer Embedding:** ขับเคลื่อนด้วย `SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")` แปลงประโยคเป็นเวกเตอร์ 384 มิติ เข้าใจภาษาพูด แสลง และประโยคเปรียบเปรยอย่างแม่นยำ
   - **150+ Typo Correction Dictionary:** คลังคำแก้คำพิมพ์ผิดเฉพาะทาง 150+ คำ (กาเเฟ, ชาเขีบว, เวนตี้, ครัวซองค์ ฯลฯ)
   - **RapidFuzz Fuzzy Matcher:** ดักจับชื่อเมนูใกล้เคียงด้วย Levenshtein Distance (Threshold >= 70%)
   - **Accuracy 100.00% & Latency ~5.3 ms** ผ่าน 36 Benchmark Test Cases ทั้งหมด

4. **🛍️ Interactive 2-Step Ordering & Dynamic Size Pricing**:
   - **2-Step Order Flow:** เมื่อระบุชื่อเมนูเจาะจง บอทจะส่งการ์ดรายละเอียดพร้อมปุ่มให้กดเลือกขนาดแก้วจริงก่อนสั่ง
   - **Dynamic Price Mapper:** คำนวณราคาและออกใบเสร็จ (Order Receipt) ตรงตามขนาดแก้วจริง: `Solo/Doppio` หรือ `Tall/Grande/Venti`

5. **📱 รองรับ LINE Full-Stack UX (Rich Menu + Quick Reply + Flex UI)**:
   - **6-Grid Rich Menu**: เมนูลัด 6 ช่อง กราฟิกคมชัด สั่งงานได้ในคลิกเดียว (`setup_rich_menu.py`)
   - **Quick Reply Chips**: เมนูแนะนำวันนี้, กาแฟสด, เบเกอรี่, โปรโมชั่นเด็ด, วิธีการใช้งาน, บาริสต้าปากแซ่บ
   - **LINE Flex Carousel & Detail**: การ์ดแสดงราคาทุกขนาด แคลอรี่ และปุ่มกดสั่งซื้อเปิดสู่หน้าเว็บทันที

---

## 🏗️ สถาปัตยกรรมโครงสร้างโปรเจกต์ (Project Architecture)

```
starbug/
├── app.py                     # เซิร์ฟเวอร์หลัก Flask (LINE Webhook /callback + Web Simulator API)
├── config.py                  # ค่ากำหนดระบบ และ LINE Channel Secret / Token
├── setup_rich_menu.py         # สคริปต์สร้างและลงทะเบียน LINE Rich Menu อัตโนมัติ
├── docs/                      # เอกสารอธิบายสถาปัตยกรรมและฟีเจอร์ฉบับละเอียด
│   └── system_architecture_and_features.md
├── data/
│   ├── scraper.py             # Data Loader & Scraper โหลดข้อมูลเมนูพร้อม Hot-Reload
│   ├── cleaner.py             # Data Normalizer & Attribute Cleaner
│   └── starbucks_menu.json    # ฐานข้อมูล 64 เมนูแท้ (ราคาแยกไซส์, แคลอรี่, หมวดหมู่, ภาพ CDN)
├── nlp/
│   ├── normalizer.py          # PyThaiNLP Normalizer และพจนานุกรมแก้คำสะกดผิด
│   ├── intents.py             # กำหนด Intent Types
│   ├── entity_extractor.py    # สกัดราคา (Min/Max), ขนาดแก้ว (Tall/Grande/Venti), รสชาติ, หมวดหมู่
│   ├── bert_classifier.py     # BERT-based Semantic Vector Space Intent Classifier
│   ├── engine.py              # NLP Matcher (Longest Substring Match + RapidFuzz Scorer)
│   └── funny_features.py      # บทสนทนาฮาๆ สไตล์ภารตะ (บาริสต้าปากแซ่บ)
├── recommender/
│   ├── filter_engine.py       # Multi-criteria Filter (งบประมาณ, ประเภท, กาแฟ/ขนม, รสชาติ)
│   └── fair_randomizer.py     # Top-5 Anti-Repetition Buffer สุ่มกระจายตัวเป็นธรรม
├── line_ui/
│   ├── flex_carousel.py       # LINE Flex Carousel การ์ดเมนู
│   ├── flex_detail.py         # LINE Flex Card แสดงราคาทุกไซส์และแคลอรี่
│   ├── flex_receipt.py        # LINE Flex Card ใบเสร็จสั่งซื้อ Dynamic Price
│   ├── flex_promo.py          # LINE Flex Carousel โปรโมชั่น
│   ├── quick_replies.py       # ปุ่ม Quick Reply ลอยด้านล่าง 5 ปุ่ม
│   └── rich_menu.py           # ตัวสร้างรูปภาพ Rich Menu 2500x1686
├── web/                       # Web Chat Simulator สำหรับทดสอบผ่านบราวเซอร์
│   ├── templates/index.html   # หน้าแชทจำลอง LINE บนมือถือ
│   └── static/
│       ├── css/style.css      # Starbug Premium Theme (#006241 Deep Green & #CBA258 Gold)
│       └── js/chat.js         # Chat Frontend Logic & Real-time NLP Diagnostics
├── tests/                     # ชุดทดสอบอัตโนมัติ (Automated Unit Tests)
│   ├── test_scraper_robustness.py  # Checkpoint 1: ความทนทานของ Data Pipeline
│   ├── test_nlp_benchmark.py       # Checkpoint 2: Benchmark Latency & Accuracy 100%
│   └── test_fairness.py            # Checkpoint 3: Randomization Fairness Audit
└── README.md
```

---

## 🚀 วิธีการติดตั้งและเริ่มต้นใช้งาน (Setup & Execution)

### 1. ติดตั้ง Dependencies
```powershell
# เปิดใช้งาน Virtual Environment (ถ้ามี)
.\venv\Scripts\activate

# ติดตั้งแพ็กเกจที่จำเป็น
pip install -r requirements.txt
```

### 2. ตั้งค่า LINE Credentials (ในไฟล์ `config.py` หรือ `.env`)
```python
LINE_CHANNEL_SECRET = "your_channel_secret"
LINE_CHANNEL_ACCESS_TOKEN = "your_channel_access_token"
```

### 3. รันสร้าง Rich Menu บน LINE (ทำเพียงครั้งเดียว)
```powershell
python setup_rich_menu.py
```

### 4. รันเซิร์ฟเวอร์หลัก (Flask Application)
```powershell
python app.py
```
- ทดสอบผ่าน **Web Chat Simulator**: เข้าบราวเซอร์ที่ **`http://localhost:5000`**

### 5. เชื่อมต่อกับ LINE Webhook ผ่าน Cloudflare Tunnel
```powershell
cloudflared tunnel --url http://localhost:5000
```
- นำ URL ที่ได้ (เช่น `https://xxxx.trycloudflare.com/callback`) ไปใส่ในช่อง **Webhook URL** ใน [LINE Developers Console](https://developers.line.biz/)

---

## 📊 ผลการทดสอบเกณฑ์ชี้วัด (Verification Benchmarks)

| หัวข้อการทดสอบ | รายละเอียดและเป้าหมาย | ผลการทดสอบจริง | สถานะ |
|---|---|---|---|
| **1. Scraping & Data Integrity** | ทดสอบความทนทานต่อ HTML ข้อมูลราคาขาดหาย และความพร้อมของไฟล์ภาพ | ผ่านการทดสอบ 100% มีรูปภาพครบทั้ง 64 รายการ | ✅ PASS |
| **2. NLP Accuracy & Speed** | ทดสอบ 35 Test Cases (คำแสลง, คำสะกดผิด, เงื่อนไขหลายชั้น) | **Accuracy: 100.00%** (เป้าหมาย >85%)<br>**Avg Latency: ~3.6 ms** (เป้าหมาย <1,500 ms) | ✅ PASS |
| **3. Randomization Fairness** | จำลอง Monte Carlo 100+ รอบ เพื่อตรวจสอบการกระจายตัวของ Top-5 | **Coverage: 100.0%** กระจายตัวครบทุกเมนู ไม่ติดลูปซ้ำ | ✅ PASS |

### คำสั่งรันการทดสอบทั้งหมด:
```powershell
python -m unittest discover tests
```

---

## 💬 ตัวอย่างคำสั่งที่ระบบรองรับ (Sample Commands)

- ☕ **ค้นหาตามหมวดหมู่:** *"ขอดูกาแฟ", "มีชาเขียวมัทฉะอะไรบ้าง", "ขอดูเมนูปั่น", "มีขนมเบเกอรี่อะไรบ้าง"*
- 💸 **กรองตามงบประมาณ:** *"งบไม่เกิน 150 บาท", "ราคาต่ำกว่า 170", "มีเมนูกาแฟไม่เกิน 140 ไหม"*
- 🔍 **ดูรายละเอียด & แคลอรี่:** *"ขอดูรายละเอียด จาวา ชิพ แฟรปปูชิโน่", "ไช ที กี่แคล"*
- 🛍️ **สั่งซื้อแยกขนาดแก้ว:** *"สั่งซื้อ Iced Caffe Americano ขนาด Venti", "สั่งซื้อ เอสเพรสโซ่ มัคคิอาโต ขนาด Doppio"*
- 🏷️ **ล่าส่วนลด:** *"มีโปรโมชั่นอะไรเด็ดๆ วันนี้", "วันนี้มี 1 แถม 1 ไหม"*
- ⭐ **คิดไม่ออก:** *"เมนูแนะนำวันนี้", "สุ่มเมนูให้หน่อย ไม่อยากคิด"*
- 🤣 **หาเรื่องโดนแซว:** *"แซวฉันหน่อย บาริสต้าปากแซ่บ"*
