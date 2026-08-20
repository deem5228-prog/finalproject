# 🥚 Egg Yolk Color Predictor

**การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่สำหรับทำนายคะแนนสีไข่แดงของไข่ไก่จากภาพถ่าย**
*Development of a Mobile Application for Predicting Egg Yolk Color Score from Photographs*

โปรเจคปริญญานิพนธ์ สาขาวิชาวิทยาการคอมพิวเตอร์ ภาควิชาคอมพิวเตอร์ มหาวิทยาลัยศิลปากร
ภาคการศึกษาต้น ปีการศึกษา 2569

---

## ภาพรวม (Overview)

แอปพลิเคชันมือถือที่ทำนาย **คะแนนพัดสีไข่แดง (Yolk Color Fan, 1-15)** จากภาพถ่ายที่ผู้ใช้ถ่ายหรือเลือกจากคลังภาพ แทนการเทียบสีด้วยสายตามนุษย์หรือใช้เครื่องมือวัดค่าสีราคาสูงอย่าง Chromameter/Spectrophotometer

แอป Flutter ครอบภาพเฉพาะบริเวณไข่แดงแล้ว**อัปโหลดไฟล์ภาพ**ไปยัง Backend ซึ่งสกัดค่าสี RGB เฉลี่ยและแปลงเป็นระบบสี CIELAB ด้วย Python ก่อนทำนายคะแนนด้วยแบบจำลอง Machine Learning โดยเปรียบเทียบแบบจำลอง 5 รูปแบบ (Linear Regression เป็น baseline ตามงานวิจัยต้นแบบ, Ridge Regression, Random Forest, Gradient Boosting, SVR — และอาจเพิ่ม Gaussian Process Regression เป็นตัวเสริม) ประเมินด้วย Stratified K-Fold Cross-Validation แล้วคัดเลือกตัวที่แม่นยำที่สุดไปใช้งานจริง

**งานอ้างอิง:** "การวัดค่าสีไข่แดงของไข่ไก่จากภาพถ่ายด้วยสมการการถดถอยเชิงเส้นพหุคูณ" — The 10th Asia Undergraduate Conference on Computing (AUC2), 2022 (เป้าหมาย R² ≥ 0.7440 เทียบกับงานนี้)

## สถาปัตยกรรมระบบ

```
📱 Flutter App  ──(POST /predict-image, Multipart: cropped image file)──▶  🐍 FastAPI Backend
                ◀──────(JSON: predicted_score, raw_score, rgb, cielab)──────

Flutter: ถ่าย/เลือกภาพ → ครอบเฉพาะไข่แดง → อัปโหลดไฟล์ภาพไปที่ Backend
Backend: รับภาพ → สกัด RGB เฉลี่ย (Python) → แปลงเป็น CIELAB (Python) → ยิงเข้าโมเดล ML
         ที่เทรนไว้แล้ว → ส่งคะแนนทำนาย + ค่าสีที่สกัดได้กลับไปให้แอปแสดงผล
```

> **หมายเหตุสถาปัตยกรรม:** ค่าสีทั้งหมด (RGB → CIELAB) คำนวณอยู่ที่ Backend (Python) เพียงจุดเดียว
> ทั้งตอนเตรียมข้อมูลเทรนโมเดลและตอนใช้งานจริง — ใช้โค้ดชุดเดียวกัน ไม่มีสูตรสีซ้ำสองภาษาแล้ว
> จึงไม่มีความเสี่ยงเรื่อง train/serve skew จากสูตรคำนวณไม่ตรงกัน (ไม่ต้องมี verification step
> ข้ามภาษาแบบที่เคยออกแบบไว้ก่อนหน้านี้อีกต่อไป)

โมเดลเทรนแยกต่างหากใน `model_dev/` (ไม่ใช่ real-time) แล้วส่งไฟล์โมเดลที่ดีที่สุดเข้ามาให้ backend โหลดใช้งาน

## Tech Stack

| ส่วน | เทคโนโลยี |
|---|---|
| Mobile App | Flutter (Dart), รองรับ Android 8.0 (API 26)+ |
| Backend API | FastAPI, Pydantic, **python-multipart** (รับไฟล์ภาพแบบ multipart/form-data) |
| Image/Color processing | Pillow (PIL) + NumPy + scikit-image — โค้ดชุดเดียวใช้ทั้งใน `model_dev/` (เตรียมข้อมูลเทรน) และ `egg_api/` (ใช้งานจริง) |
| Mobile-side | `image_cropper` (ครอบภาพ), `http`/`dio` (อัปโหลด multipart) — ไม่มีโค้ดคำนวณสีฝั่ง Dart แล้ว |
| Machine Learning | scikit-learn (Linear Regression, Ridge, Random Forest, Gradient Boosting, SVR, Gaussian Process), joblib |
| Model dev | Jupyter Lab |

## โครงสร้างโปรเจค

```
egg_yolk_project/
├── model_dev/                      # เทรน & เปรียบเทียบโมเดล (ไม่ deploy)
│   ├── data/
│   │   ├── raw_images/             # ภาพไข่แดงที่ครอบแล้ว
│   │   ├── labels.csv              # image_filename, fan_score
│   │   └── features.csv            # + R,G,B,L,a,b ที่สกัดแล้ว
│   ├── color_service.py            # RGB→CIELAB (โค้ดเดียวกับใน egg_api/services/)
│   ├── build_features.py
│   ├── train_compare_models.ipynb
│   ├── export_best_model.py
│   └── model.pkl                    # โมเดลที่ดีที่สุด (generated)
│
├── egg_api/                         # Backend ที่ deploy จริง
│   ├── main.py
│   ├── schemas.py
│   ├── routers/predict.py           # POST /predict-image
│   ├── services/
│   │   ├── color_service.py         # RGB extraction + CIELAB conversion (canonical copy)
│   │   └── predict_service.py
│   └── model/model.pkl              # copy จาก model_dev
│
└── egg_yolk_app/                     # Flutter mobile app
    └── lib/
        ├── main.dart
        ├── models/prediction_result.dart
        ├── services/api_service.dart # อัปโหลดภาพแบบ multipart เท่านั้น
        └── screens/
            ├── splash_screen.dart
            ├── home_screen.dart
            ├── camera_screen.dart
            ├── crop_screen.dart
            ├── result_screen.dart
            └── detail_screen.dart
```

## เริ่มต้นใช้งาน (Getting Started)

### Prerequisites
- Python 3.10+
- Flutter SDK (stable channel) + Android Studio (สำหรับ Android SDK/emulator)
- Git

### 1. Model development (`model_dev/`)
```bash
cd model_dev
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python build_features.py          # ต้องมี data/raw_images/ + data/labels.csv ก่อน
jupyter lab train_compare_models.ipynb   # เทรน+เทียบโมเดล เลือกตัวที่ดีที่สุดเอง
python export_best_model.py       # ได้ model.pkl
```

### 2. Backend (`egg_api/`)
```bash
cd egg_api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
เช็คว่ารันอยู่: `curl http://localhost:8000/` ควรได้ `{"status": "ok"}`

### 3. Mobile App (`egg_yolk_app/`)
```bash
cd egg_yolk_app
flutter pub get
flutter run   # เลือก emulator/device
```
> หมายเหตุ: `api_service.dart` ตั้ง `baseUrl` เป็น `http://10.0.2.2:8000` (alias ของ localhost บน Android emulator) — ถ้าทดสอบบนมือถือจริง ต้องเปลี่ยนเป็น IP จริงของเครื่องที่รัน backend

## API Reference

**`POST /predict-image`** — รับไฟล์ภาพไข่แดงที่ครอบแล้ว คืนค่าสีที่สกัดได้และคะแนนทำนาย

```bash
curl -X POST http://localhost:8000/predict-image \
  -F "file=@cropped_yolk.jpg"
```

```json
{
  "predicted_score": 12,
  "raw_score": 11.96,
  "rgb": {"r": 226, "g": 131, "b": 23},
  "cielab": {"l": 64.2, "a": 29.8, "b": 65.9}
}
```

## การประเมินโมเดล

เกณฑ์: R², MAE, RMSE, และสัดส่วนที่ทำนายคลาดเคลื่อนไม่เกิน 1 ระดับจากคะแนนจริง — เป้าหมาย **R² ≥ 0.7440**

| Model | R² (mean ± sd) | MAE | RMSE | ±1 Level Accuracy |
|---|---|---|---|---|
| Linear Regression | – | – | – | – |
| Ridge Regression | – | – | – | – |
| Random Forest | – | – | – | – |
| Gradient Boosting | – | – | – | – |
| SVR | – | – | – | – |
| Gaussian Process *(เสริม)* | – | – | – | – |

*ประเมินด้วย Stratified 5-Fold CV (แบ่งตามช่วงคะแนน ไม่ใช่ train/test split ครั้งเดียว) — กรอกผลจริงหลังรัน `train_compare_models.ipynb`*

## ขอบเขตและข้อจำกัด

- รองรับเฉพาะภาพไข่แดงที่แยกออกจากไข่ขาวแล้ว ถ่ายภายใต้สภาพแสงที่เหมาะสม
- ไม่ครอบคลุมการวิเคราะห์ภาพไข่ทั้งฟอง หรือการประเมินคุณภาพไข่ด้านอื่น
- รองรับเฉพาะ Android (API 26+) ยังไม่รองรับ iOS
- การสกัดค่าสีทั้งหมดอยู่ที่ Backend (Python) จุดเดียว — ภาพต้องอัปโหลดผ่านเครือข่ายทุกครั้งที่ทำนาย (ต่างจากแบบคำนวณในเครื่องที่ทำงานได้แม้ไม่มีอินเทอร์เน็ต)

## สถานะโปรเจค

**ยังไม่มีส่วนไหนถูกสร้าง/รันจริงเลย ณ ตอนนี้ — มีแค่ dataset กับไฟล์ planning (README + prompt pack)**

- [x] เก็บ dataset (ภาพไข่แดง + คะแนนพัดสีจริง)
- [ ] `color_service.py` (Python) + unit test
- [ ] สร้าง `features.csv`
- [ ] เทรน + เทียบโมเดล ≥3 แบบ
- [ ] Export โมเดลที่ดีที่สุด
- [ ] Backend: `services/color_service.py` (รับภาพ → RGB → CIELAB) ใน `egg_api/`
- [ ] Backend: `POST /predict-image` endpoint รับภาพ ทำนายคะแนน
- [ ] Flutter app ครบ flow (ถ่าย/ครอบ/อัปโหลดภาพ — ไม่ต้องคำนวณสีเอง)
- [ ] รวมโมเดลจริงเข้า backend
- [ ] Integration testing (smoke test)
- [ ] เขียนเล่มปริญญานิพนธ์

## ผู้จัดทำ

- **ผู้รับผิดชอบโครงงาน:** นายพงศธรณ์ วิสูตรรุจิรา (660710723)
- **อาจารย์ที่ปรึกษา:** ผู้ช่วยศาสตราจารย์ ดร.อรวรรณ เชาวลิต
