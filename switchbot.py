import time
import hashlib
import hmac
import base64
import requests


class Auth:
    def __init__(self, token: str, secret: str):
        self.token = token
        self.secret = secret

    def make_sign(self, timestamp: int, nonce: str = ""):
        string_to_sign = f"{self.token}{timestamp}{nonce}"
        secret_bytes = bytes(self.secret, "utf-8")
        string_to_sign_bytes = bytes(string_to_sign, "utf-8")
        sign = base64.b64encode(
            hmac.new(
                secret_bytes,
                msg=string_to_sign_bytes,
                digestmod=hashlib.sha256
            ).digest()
        )
        return sign


class Client:
    base_url = "https://api.switch-bot.com"

    def __init__(self, auth: Auth):
        self.auth = auth

    def make_request_header(self):
        timestamp = int(round(time.time() * 1000))
        sign = self.auth.make_sign(timestamp)
        headers = {
            "Authorization": self.auth.token,
            "sign": sign,
            "t": str(timestamp),
            "nonce": "",
        }
        return headers

    def fetch_devices(self):
        devices_url = f"{self.base_url}/v1.1/devices"
        headers = self.make_request_header()
        res = requests.get(devices_url, headers=headers)
        if res.status_code == 200:
            return res.json()
        else:
            res.raise_for_status()

    def send_device_command(self, device_id: str, command: str):
        url = f"{Client.base_url}/v1.1/devices/{device_id}/commands"
        headers = self.make_request_header()
        data = {
            "commandType": "command",
            "command": command,
            "parameter": "default",
        }
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            return res.json()
        else:
            res.raise_for_status()


class DoorClient(Client):
    def __init__(self, auth: Auth, device_id: str):
        self.auth = auth
        self.device_id = device_id

    def lock(self):
        self.send_device_command(self.device_id, "lock")

    def unlock(self):
        self.send_device_command(self.device_id, "unlock")
