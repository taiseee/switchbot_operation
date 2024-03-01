import time
import hashlib
import hmac
import base64
import requests
import json

# open token
token = 'efde79485d13de0bd56c96b8d87907f7d5526961006ee8dbfad7283b88069983873b64454db42e1a487378a9388a3c44' # copy and paste from the SwitchBot app V6.14 or later
# secret key
secret = '4b4d4c7d1c34385cc094a49fc1d37f4e' # copy and paste from the SwitchBot app V6.14 or later
nonce = ''
t = int(round(time.time() * 1000))
string_to_sign = '{}{}{}'.format(token, t, nonce)

string_to_sign = bytes(string_to_sign, 'utf-8')
secret = bytes(secret, 'utf-8')

sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
print ('Authorization: {}'.format(token))
print ('t: {}'.format(t))
print ('sign: {}'.format(str(sign, 'utf-8')))
print ('nonce: {}'.format(nonce))

def make_sign(token: str,secret: str):
    nonce = ''
    t = int(round(time.time() * 1000))
    string_to_sign = bytes(f'{token}{t}{nonce}', 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign, str(t), nonce

def make_request_header(token: str,secret: str) -> dict:
    sign,t,nonce = make_sign(token, secret)
    headers={
            "Authorization": token,
            "sign": sign,
            "t": str(t),
            "nonce": nonce
        }
    return headers

base_url = 'https://api.switch-bot.com'

def get_device_list(deviceListJson='deviceList.json'):
    # tokenとsecretを貼り付ける
    token = "efde79485d13de0bd56c96b8d87907f7d5526961006ee8dbfad7283b88069983873b64454db42e1a487378a9388a3c44"
    secret = "4b4d4c7d1c34385cc094a49fc1d37f4e"

    devices_url = base_url + "/v1.1/devices"

    headers = make_request_header(token, secret)

    try:
        # APIでデバイスの取得を試みる
        res = requests.get(devices_url, headers=headers)
        res.raise_for_status()

        print(res.text)
        deviceList = json.loads(res.text)
        # 取得データをjsonファイルに書き込み
        with open(deviceListJson, mode='wt', encoding='utf-8') as f:
            json.dump(deviceList, f, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

#鍵のロック
def lock(deviceId: str, token: str, secret: str):
    token = "efde79485d13de0bd56c96b8d87907f7d5526961006ee8dbfad7283b88069983873b64454db42e1a487378a9388a3c44"
    secret = "4b4d4c7d1c34385cc094a49fc1d37f4e"

    devices_url = base_url + "/v1.1/devices/" + deviceId + "/commands"
    headers = make_request_header(token, secret)
    data={
            "commandType": "command",
            "command": "lock",
            "parameter": "default",
        }
    try:
        # ロック
        res = requests.post(devices_url, headers=headers, json=data)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

#鍵のアンロック
def unlock(deviceId: str, token: str, secret: str):
    token = "efde79485d13de0bd56c96b8d87907f7d5526961006ee8dbfad7283b88069983873b64454db42e1a487378a9388a3c44"
    secret = "4b4d4c7d1c34385cc094a49fc1d37f4e"

    devices_url = base_url + "/v1.1/devices/" + deviceId + "/commands"
    headers = make_request_header(token, secret)
    data={
            "commandType": "command",
            "command": "unlock",
            "parameter": "default",
        }
    try:
        # アンロック
        res = requests.post(devices_url, headers=headers, json=data)
        res.raise_for_status()
        print(res.text)
        
    except requests.exceptions.RequestException as e:
        print('response error:',e)
        
def get_header(event, context):
	try:
		# パラメータ設定
		# ヘッダー項目取得
		deviceId = event['headers']['deviceid']

		# 取得結果を返却
		return {
                'deviceId': deviceId,
		}
	except Exception as e:
		# エラー
		print(e)
