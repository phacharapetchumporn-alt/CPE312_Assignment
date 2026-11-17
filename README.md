# California Housing — Model as a Service (Flask & Docker)

ระบบบริการโมเดล Machine Learning (Model as a Service) สำหรับทำนายราคาบ้านในแคลิฟอร์เนีย (California Housing Dataset) พัฒนาด้วย Flask, Scikit-learn (Random Forest) และ Containerize ด้วย Docker

---

## 1. โครงสร้างโปรเจกต์ (Project Structure)

```text
ml_service/
├── Dockerfile              # Docker configuration สำหรับ build production container
├── requirements.txt        # รายการ Python dependencies
├── train_model.py          # สคริปต์ฝึกสอนโมเดล Random Forest และเซฟ model.pkl
├── app.py                  # แอปพลิเคชัน Flask (REST API & Web UI)
├── templates/
│   └── main.html           # หน้าเว็บ UI สำหรับทดสอบทำนายผล
├── model/                  # โฟลเดอร์เก็บ model.pkl (สร้างอัตโนมัติจากการเทรน)
│   └── model.pkl
├── .gitignore              # ละเว้นไฟล์ขนาดใหญ่ (เช่น model.pkl) และ cache
└── README.md               # เอกสารประกอบโครงการ
```

---

## 2. วิธีการติดตั้งและรันด้วย Docker (Production)

### 2.1 สร้าง Docker Image
เปิด Terminal หรือ PowerShell แล้วเข้าไปที่โฟลเดอร์ `ml_service`:
```bash
cd D:\CPE312\ml_service
docker build -t ds-ml-service .
```
*(ในขั้นตอน build จะมีการติดตั้ง dependencies และรัน `python train_model.py` เพื่อสร้างโมเดลโดยอัตโนมัติ)*

### 2.2 รัน Docker Container
```bash
docker run --rm -p 5000:5000 ds-ml-service
```
หากพอร์ต 5000 ใช้งานอยู่ สามารถเปลี่ยนเป็นพอร์ตอื่น เช่น:
```bash
docker run --rm -p 8080:5000 ds-ml-service
```

---

## 3. วิธีการรันบน Local Environment (สำหรับการพัฒนา/ทดสอบ)

1. สร้างและเปิดใช้งาน Virtual Environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. ติดตั้ง Dependencies:
```powershell
pip install flask scikit-learn joblib pandas numpy
```

3. สั่งเทรนโมเดล:
```powershell
python train_model.py
```
*(จะได้ไฟล์โมเดลถูกบันทึกไว้ที่ `model/model.pkl`)*

4. รันเซิร์ฟเวอร์ Flask:
```powershell
python app.py
```

---

## 4. การทดสอบและเรียกใช้งาน (Endpoints)

| Endpoint | Method | คำอธิบาย |
| :--- | :---: | :--- |
| `/` | `GET`, `POST` | หน้าเว็บแบบฟอร์มรับค่า 8 ฟีเจอร์และแสดงผลการทำนาย |
| `/health` | `GET` | ตรวจสอบสถานะการทำงานของบริการ และแสดงรายชื่อฟีเจอร์ |
| `/predict` | `POST` | REST API สำหรับส่งค่าฟีเจอร์แบบ JSON และรับผลการทำนาย |

### 4.1 ทดสอบผ่าน Web Browser
- เปิดเบราว์เซอร์ไปที่: `http://127.0.0.1:5000/`
- สามารถกดปุ่ม **"Use sample values"** เพื่อกรอกค่าตัวอย่างอัตโนมัติ
- กดปุ่ม **"Predict"** เพื่อดูผลการประเมินราคาบ้าน (หน่วย $100,000s)

### 4.2 ตรวจสอบ Health Check
- URL: `http://127.0.0.1:5000/health`
- ผลลัพธ์ตัวอย่าง:
```json
{
  "features": [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude"
  ],
  "ok": true
}
```

### 4.3 ทดสอบ REST API ด้วย PowerShell
ส่งค่าฟีเจอร์ 8 ค่า:
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"features":[8.3, 25.0, 6.0, 1.0, 1200, 3.0, 34.2, -118.3]}'
```

**ผลลัพธ์ที่ได้:**
```json
{
  "prediction": 4.029472199999998
}
```
*(ประมาณ 4.03 หรือราว $403,000)*

---

## 5. การส่งงาน (Submission)

1. ทำการ Commit และ Push โค้ดขึ้น GitHub Repository
   *(ตรวจสอบให้แน่ใจว่าไฟล์ `.gitignore` ไม่ได้นำ `model/model.pkl` หรือ `.venv` ขึ้นไป)*
2. ถ่ายภาพหน้าจอ (Screenshot) ของหน้าเว็บ `http://127.0.0.1:5000/` ขณะแสดงผลการทำนาย
3. ส่งลิงก์ GitHub Repository ผ่าน Google Form:
   - [แบบฟอร์มส่งงาน: Assignment การสร้าง Model as a Service ด้วย Flask และ Docker](https://forms.gle/D8UCryawXbEn4FSe7)
