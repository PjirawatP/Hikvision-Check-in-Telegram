# Hikvision Event Listener + Telegram Notify

โปรเจกต์นี้ใช้สำหรับรับ **Event การสแกนใบหน้า จาก Hikvision Face Recognition** จากนั้นจะ **ผูก Event + รูปภาพ** และส่งแจ้งเตือนไปยัง **Telegram Bot**

---

## Model ที่ทดสอบแล้ว
    * DS-K1T672MW

---

## ⚙️ Prerequisites

* Python **3.10+**
* Docker (แนะนำ)
* Telegram Bot Token
* Telegram Chat ID

---

## DEVICE_INFO

```src/main.py
DEVICES = [
    {
        "name": "DEVICE_NAME",
        "ip": "DEVICE_IP",
        "port": "DEVICE_PORT",
        "username": "DEVICE_USERNAME",
        "password": "DEVICE_PASSWORD"
    },
    {
        "name": "DEVICE_NAME",
        "ip": "DEVICE_IP",
        "port": "DEVICE_PORT",
        "username": "DEVICE_USERNAME",
        "password": "DEVICE_PASSWORD"
    }
]
```

---
## Environment Variables

```env
# ========== TELEGRAM ==========
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
```

---

## Run ด้วย Python (Local)

### สร้าง Virtual Environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / Mac**

```bash
source .venv/bin/activate
```

---

### 2 ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

---

### 3 Run Application

```bash
python src/main.py
```

ถ้าสำเร็จ:

```text
[DeviceName1] Connected
[DeviceName2] Connected
```

---

## Run ด้วย Docker (Recommended)

### Build & Run

```bash
docker compose up -d --build
```

ดู log:

```bash
docker compose logs -f
```