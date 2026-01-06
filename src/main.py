import json, os, requests, threading ,time

from datetime import datetime
from dotenv import load_dotenv
from io import BytesIO


load_dotenv()

DEVICES = [
    {
        "name": "DEVICE_NAME",
        "ip": "DEVICE_IP",
        "port": "DEVICE_PORT",
        "username": "DEVICE_USERNAME",
        "password": "DEVICE_PASSWORD"
    }
]

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")



def run_device(device):
    event_listener = EventListener(
        device["name"],
        device["ip"],
        device["port"],
        device["username"],
        device["password"],
        telegram_notify = TelegramNotify(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    )

    if event_listener.test_connection():
        while True:
            event_listener.listening()



class EventListener:
    def __init__(self, device_name, device_ip, device_port, device_username, device_password, telegram_notify):
        self.device_name = device_name
        self.base_url = f"http://{device_ip}:{device_port}/ISAPI"
        self.auth = requests.auth.HTTPDigestAuth(device_username, device_password)
        self.telegram_notify = telegram_notify
        self.last_event = None


    def test_connection(self):
        request_url = f"{self.base_url}/System/deviceInfo"

        try:
            response = requests.get(request_url,  auth = self.auth, timeout = 5)

            if response.status_code == 200:
                print(f"[{self.device_name}] Connected")

                return True

        except Exception:
            pass

        print(f"[{self.device_name}] Connection failed")

        return False

    
    def listening(self):
        request_url = f"{self.base_url}/Event/notification/alertStream"

        try:
            with requests.get(request_url, auth = self.auth, stream = True, timeout = None) as response:
                boundary = response.headers.get("Content-Type").split("boundary=")[-1]

                buffer = b""

                for chunk in response.iter_content(chunk_size = 1024):
                    buffer += chunk
                    
                    while b"--" + boundary.encode() in buffer:
                        part, buffer = buffer.split(b"--" + boundary.encode(), 1)

                        self._handle_part(part)

        except requests.exceptions.RequestException as e:
            print(f"[{self.device_name}] stream error: {e}")

            time.sleep(3)


    def _handle_part(self, part: bytes):
        if b"\r\n\r\n" not in part:
            return

        header, body = part.split(b"\r\n\r\n", 1)
        header_text = header.decode(errors = "ignore")

        if "application/json" in header_text:
            try:
                data = json.loads(body.decode(errors = "ignore"))
                
                print(data)

                iso_time = data.get("dateTime")
                dt = datetime.fromisoformat(iso_time) if iso_time else None
                fmt_time = dt.strftime("%d/%m/%Y %H:%M:%S") if dt else "-"

                event = data.get("AccessControllerEvent", {})
                name = event.get("name")

                if name and str(name).strip():
                    self.last_event = {
                        "name": name,
                        "time": fmt_time
                    }

                    message = (
                        f"เครื่อง: {self.device_name}\n"
                        f"ชื่อ: {name}\n"
                        f"ลงชื่อเข้าเมื่อ: {fmt_time}"
                    )

                    self.telegram_notify.send_message(message)
            
            except Exception as e:
                print(f"[{self.name}] JSON error: {e}")
    
        elif "image/jpeg" in header_text:
            if self.last_event:
                self.telegram_notify.send_photo(body)
                self.last_event = None



class TelegramNotify:
    def __init__(self, telegram_bot_token, telegram_chat_id):
        self.telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}"
        self.telegram_chat_id = telegram_chat_id


    def send_message(self, message):
        try:
            requests.post(
                f"{self.telegram_api_url}/sendMessage",
                json = {
                    "chat_id": self.telegram_chat_id,
                    "text": message
                }
            )

        except Exception as e:
            print("Telegram message error:", e)


    def send_photo(self, image_bytes):
        try:
            requests.post(
                f"{self.telegram_api_url}/sendPhoto",
                data = {
                    "chat_id": self.telegram_chat_id
                },
                files = {
                    "photo": ("face.jpg", BytesIO(image_bytes))
                }
            )

        except Exception as e:
            print("Telegram photo error:", e)



if __name__ == "__main__":
    for device in DEVICES:
        threading.Thread(
            target = run_device,
            args = (device,),
            daemon = False
        ).start()

    print("Listening all devices...")

    while True:
        time.sleep(1)
