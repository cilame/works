# -*- coding: UTF-8 -*-
import time
import urllib
import requests
import json
import hashlib
import base64
import sys

import config

def asr(filename, rate=16000):
    with open(filename, 'rb') as f:
        content = f.read()
    base64_audio = base64.b64encode(content)
    body = urllib.parse.urlencode({'audio': base64_audio})
    url = 'http://api.xfyun.cn/v1/service/v1/iat'

    if rate == 16000: engine_type = "sms16k"
    if rate == 8000 : engine_type = "sms8k"
    param = {"engine_type": engine_type, "aue": "raw"}

    x_appid = config.xunfei.APPID
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode())
    x_time = int(int(round(time.time() * 1000)) / 1000)

    api_key = config.xunfei.APIKey
    x_checksum = hashlib.md5(api_key.encode() + str(x_time).encode() + x_param).hexdigest()
    x_header = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'X-Appid': x_appid,
                'X-CurTime': str(x_time),
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = requests.post(url, body, headers=x_header)
    data = json.loads(req.content.decode("utf-8")).get("data")
    if data:
        return True,data
    else:
        return False,req.text

if __name__ == '__main__':
    # 4 test
    filename = "../file4test/c7678235123242079a7c7658b478bd46.wav"
    v = asr(filename,8000)
    print(v)
