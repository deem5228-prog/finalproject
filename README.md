# 🥚 Egg Yolk Color Predictor

**การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่สำหรับทำนายคะแนนสีไข่แดงของไข่ไก่จากภาพถ่าย**  
*Development of a Mobile Application for Predicting Egg Yolk Color Score from Photographs*

โปรเจกต์ปริญญานิพนธ์ สาขาวิชาวิทยาการคอมพิวเตอร์ ภาควิชาคอมพิวเตอร์ มหาวิทยาลัยศิลปากร  
ภาคการศึกษาต้น ปีการศึกษา 2569

---

## 📖 ภาพรวม (Overview)

แอปพลิเคชันและระบบประมวลผลสำหรับทำนาย **คะแนนพัดสีไข่แดง (DSM Yolk Color Fan ระดับ 1–15)** จากภาพถ่ายดิจิทัล แทนการเทียบสีด้วยสายตามนุษย์หรือการใช้เครื่องมือวัดค่าสีราคาสูงในห้องปฏิบัติการ

ระบบใช้แนวทาง **Digital Image Processing (DIP)** สกัดค่าสีทางกายภาพ 6 มิติ (**RGB** และ **CIELAB** ตามมาตรฐานสากล CIE D65) พร้อมเทคนิค **Center Circular Masking (รัศมี 42%)** เพื่อคัดแยกและตัดพื้นหลังโต๊ะไม้ออก $100\%$ จากนั้นป้อนเข้าสู่แบบจำลองการเรียนรู้ของเครื่อง **Support Vector Regression (SVR with RBF Kernel)** ซึ่งให้ความแม่นยำสูงถึง **$Test\ R^2 = 0.9175$ ($91.75\%$)** และความคลาดเคลื่อนเฉลี่ย **$\text{MAE} = 0.6453$ ระดับพัดสี**

---

## 🏗️ สถาปัตยกรรมระบบ (System Architecture)

```
📱 Flutter Mobile App / 🖥️ Web App
       │
       ▼ (POST /predict-image: Multipart Cropped Image)
🐍 FastAPI Backend Server (egg_api)
       │
       ├─► 🎨 color_service.py (Center Circular Masking -> RGB & CIELAB Extraction)
       ├─► 🧠 predict_service.py (StandardScaler -> SVR RBF Pipeline Model)
       │
       ▼ (JSON Response: predicted_score, raw_score, rgb, cielab, chroma, hue_angle)
📱 แสดงผลลัพธ์บนหน้าจอ (ระดับพัดสี, ค่าสี RGB, Lab, Chroma, Hue Angle)
```

---

## 🛠️ เทคโนโลยีที่ใช้ (Tech Stack)

| ส่วนของระบบ | เทคโนโลยีที่ใช้ |
|---|---|
| **Mobile Application** | Flutter (Dart), `image_cropper` (Circular Crop Style), `http` |
| **Web Interface** | HTML5, CSS3, JavaScript (Canvas Cropper Engine) |
| **Backend API** | FastAPI, Uvicorn, Pydantic, Python-Multipart |
| **Image & Color Processing** | Pillow (PIL), NumPy, scikit-image (CIE D65 Standard) |
| **Machine Learning** | scikit-learn (SVR, Random Forest, Gradient Boosting, Linear Regression, Ridge), Joblib |
| **Model Development** | Python 3.10+, Jupyter Notebook (`.ipynb`) |

---

## 📊 ผลการประเมินประสิทธิภาพโมเดล (Benchmark Results)

ประเมินด้วยวิธี **Stratified 5-Fold Cross-Validation** (แบ่งตามสัดส่วนคลาส $80/20$ บนชุดข้อมูลภาพถ่ายจริง 647 ภาพ):

```
==========================================================================================
MODEL TRAIN vs TEST COMPARISON RESULTS (Stratified 5-Fold Cross-Validation)
==========================================================================================
            Model  Train R2  Test R2  Train MAE  Test MAE  Train RMSE  Test RMSE
 SVR (RBF Kernel)    0.9295   0.9175     0.5814    0.6453      0.7915     0.8532  🏆 ชนะเลิศ
    Random Forest    0.9871   0.9087     0.2462    0.6485      0.3389     0.8923
Gradient Boosting    0.9663   0.9063     0.4209    0.6621      0.5473     0.9038
Linear Regression    0.8749   0.8718     0.8074    0.8136      1.0542     1.0645
 Ridge Regression    0.8574   0.8545     0.8775    0.8835      1.1256     1.1355
==========================================================================================

Best Performing Model: SVR (RBF Kernel) (C=10.0, epsilon=0.1, R2 = 0.9175)
```

---

## 📋 ตารางความแม่นยำรายคลาสของโมเดล SVR (Per-Class Breakdown)

```
==========================================================================================
           Model  Class (Fan Score)  Samples  Mean Pred    MAE     RMSE
------------------------------------------------------------------------------------------
SVR (RBF Kernel)                  4       36       4.29   0.3437  0.6434
SVR (RBF Kernel)                  5       41       5.48   0.7397  0.9146
SVR (RBF Kernel)                  6       49       6.14   0.6864  0.8799
SVR (RBF Kernel)                  7       42       7.29   0.7035  0.9421
SVR (RBF Kernel)                  8       64       8.26   0.5288  0.6512
SVR (RBF Kernel)                  9      105       9.06   0.6079  0.7664
SVR (RBF Kernel)                 10       99      10.02   0.6547  0.8258
SVR (RBF Kernel)                 11       75      10.77   0.6839  0.9368
SVR (RBF Kernel)                 12       33      11.68   0.8708  1.1319
SVR (RBF Kernel)                 13       21      12.66   0.9676  1.0728
SVR (RBF Kernel)                 14       33      13.47   0.7329  0.9236
SVR (RBF Kernel)                 15       49      14.61   0.5019  0.8145
==========================================================================================
```

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```
egg_yolk_project/
├── model_dev/                      # การพัฒนา ฝึกสอน และประเมินโมเดล
│   ├── data/
│   │   ├── raw_images/             # คลังภาพถ่ายไข่แดง
│   │   ├── labels.csv              # image_filename, fan_score
│   │   └── features.csv            # ฟีเจอร์สี 6 ตัวแปร (R, G, B, L*, a*, b*)
│   ├── plots/                      # รูปภาพกราฟสถิติความละเอียดสูง (300 DPI)
│   ├── color_service.py            # การสกัดสีด้วย Center Circular Masking
│   ├── build_features.py           # สคริปต์สกัดฟีเจอร์ชุดใหญ่
│   ├── train_compare_models.py     # เปรียบเทียบ 5 โมเดลด้วย 5-Fold CV
│   ├── train_compare_models.ipynb  # สมุดบันทึก Jupyter Notebook
│   ├── generate_all_plots.py       # สคริปต์สร้างรูปภาพกราฟประเมินผลทั้งหมด
│   ├── export_best_model.py        # เทรนโมเดลตัวเต็มและส่งออก model.pkl
│   └── model.pkl                   # ไฟล์สมองกล SVR Pipeline (40.5 KB)
│
├── egg_api/                        # Backend RESTful API Server
│   ├── main.py                     # จุดเริ่มต้น FastAPI Server (เปิด /web, /docs)
│   ├── schemas.py                  # Pydantic Data Models
│   ├── web_app.html                # หน้าเว็บ Web App UI สำหรับทดสอบ
│   ├── routers/predict.py          # Endpoint POST /predict-image
│   ├── services/
│   │   ├── color_service.py        # คำนวณ RGB, Lab, Chroma, Hue Angle
│   │   └── predict_service.py      # โหลด model.pkl และทำนายผล
│   └── model/model.pkl             # ไฟล์โมเดลที่ใช้งานจริง
│
└── egg_yolk_app/                   # Flutter Mobile Application
    └── lib/
        ├── main.dart
        ├── models/prediction_result.dart
        ├── services/api_service.dart
        └── screens/
            ├── splash_screen.dart
            ├── home_screen.dart
            ├── crop_screen.dart
            ├── result_screen.dart
            └── detail_screen.dart
```

---

## 🚀 วิธีการติดตั้งและรันระบบ (Getting Started)

### 1. สตาร์ต Backend API Server:
```bash
cd egg_yolk_project/egg_api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
* หน้าทดสอบ Web App: **[http://localhost:8000/web](http://localhost:8000/web)**
* หน้าเอกสาร Swagger API: **[http://localhost:8000/docs](http://localhost:8000/docs)**

### 2. รันแอปพลิเคชันมือถือ Flutter:
```bash
cd egg_yolk_project/egg_yolk_app
flutter pub get
flutter run
```

---

## 👥 ผู้จัดทำ

* **ผู้รับผิดชอบโครงงาน:** นายพงศธรณ์ วิสูตรรุจิรา (660710723)
* **อาจารย์ที่ปรึกษา:** ผู้ช่วยศาสตราจารย์ ดร.อรวรรณ เชาวลิต
