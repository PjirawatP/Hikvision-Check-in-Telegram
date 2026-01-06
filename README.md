# Hikvision Event Listener + Telegram Notify

โปรเจกต์นี้ใช้สำหรับรับ **Event การสแกนใบหน้า จาก Hikvision Face Recognition** จากนั้นจะ **ผูก Event + รูปภาพ** และส่งแจ้งเตือนไปยัง **Telegram Bot**

---

## Model ที่ทดสอบแล้ว

* DS-K1T672MW
* DS-K1T323MBFWX-E1

---

## ขั้นตอนการติดตั้ง Project

### Prerequisties

* Docker (แนะนำ)
* Python **3.12**
* Telegram Bot Token และ Chat ID

---

### Project Setup

* ดาวน์โหลด Source Code ด้วย [Git](https://git-scm.com/)

    ```
    git clone https://github.com/PjirawatP/Hikvision-Check-in-Telegram.git
    ```

* เพิ่มข้อมูลของอุปกรณ์ใน src/main.py

    ```
    DEVICES = [
        {
            "name": "DEVICE_NAME",
            "ip": "DEVICE_IP",
            "port": "DEVICE_PORT",
            "username": "DEVICE_USERNAME",
            "password": "DEVICE_PASSWORD"
        }
    ]
    ```

* หากต้องการเพิ่มอุปกรณ์สามารถทำได้ดังตัวอย่างด้านล่าง

    ```
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

* เพิ่ม Telegram Bot Token และ Chat ID ลงใน .env

    ```.env
    TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
    TELEGRAM_CHAT_ID=YOUR_CHAT_ID
    ```

---

### Telegram Bot Token & Chat ID 

* สามารถไปเอา Telegram Bot Token & Chat ID ได้ที่ [Telegram](https://web.telegram.org/a/)

    * เมื่อเข้าไปยังหน้าเว็บของ Telegram ให้ทำการเข้าสู่ระบบให้เรียบร้อย

    * จากนั้นพิมพ์ **BotFather** ในช่องค้นหา

    * คลิกเข้าไปที่ **BotFather** เพื่อทำการสนทนา

    * พิมพ์ข้อความในช่องสนทนาว่า **/newbot** และกดส่ง

    * เมื่อกดส่งไปแล้วจะได้ข้อความว่า

        ```
        Alright, a new bot. How are we going to call it? Please choose a name for your bot.
        ```

    * หลังจากนั้นให้พิมพ์ชื่อบอทของตนเอง โดยต้องมีคำว่า **bot** ต่อท้าย เช่น

        ```
        NotifyBot
        ```

    * หากสร้างบอทสำเร็จจะได้ข้อความ ดังนี้

        ```
        Done! Congratulations on your new bot. You will find it at t.me/<YOUT_BOT_NAME>. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

        Use this token to access the HTTP API:
        <YOUR_BOT_TOKEN>
        Keep your token secure and store it safely, it can be used by anyone to control your bot.

        For a description of the Bot API, see this page: https://core.telegram.org/bots/api
        ```

    * เมื่อสร้างบอทแล้วให้ทำการเข้าไปยังบอทของตนเอง และพิมพ์ข้อความบางอย่างส่งไปยังบอทของตนเอง
    
    * หลังจากนั้นให้ไปยัง

        ```
        https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
        ```

    * จะได้ข้อความแบบ JSON ดังตัวอย่างด้านล่าง

        ```
        {
            "ok": true,
            "result": [
                {
                    "update_id": 202193988,
                    "message": {
                        "message_id": 246,
                        "from": {
                            "id": <YOUR_CHAT_ID>,
                            "is_bot": false,
                            "first_name": "Unknow",
                            "language_code": "en"
                        },
                        "chat": {
                            "id": <YOUR_CHAT_ID>,
                            "first_name": "Firstname",
                            "type": "private"
                        },
                        "date": 1767681204,
                        "text": "Hello World"
                    }
                }
            ]
        }
        ```

---

### Device Setup

* DS-K1T672MW Firmware Version V3.7.0 build 231207

    * ไปที่ Configuration/Security/Privacy Settings
        
        * เปิดใช้งานในส่วนของ Authentication Result Settings และ Picture Uploading and Storage ให้หมด

        * จากนั้นกด Save

* DS-K1T323MBFWX-E1 Firmware Version V4.23.40 build 250816

    * ไปที่ Paramiter Settings/Privacy Settings

        * เปิดใช้งานในส่วนของ Authentication Result Settings และ Picture Uploading and Storage ให้หมด

        * จากนั้นกด Save

---

## ขั้นตอนการ Run Project

### Run ด้วย Python (Local)

* สร้าง Virtual Environment

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

* ติดตั้ง Dependencies

    ```bash
    pip install -r requirements.txt
    ```

* Run Application

    ```bash
    python src/main.py
    ```

---

### Run ด้วย Docker (แนะนำ)

* Build & Run

    ```bash
    docker compose up -d --build
    ```

* ดู log

    ```bash
    docker compose logs -f
    ```
