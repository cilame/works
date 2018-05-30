import os, time
import requests
import urllib
import json
import hashlib
import base64
import logging

import config

def get_sign_code(params, app_key):
    if params is None or type(params) != dict or len(params) == 0: return
    try:
        params = sorted(params.items(), key=lambda x:x[0])
        _str = ''
        for item in params:
            key = item[0]
            value = item[1]
            if value == '': continue
            _str += urllib.parse.urlencode({key: value}) + '&'
        _str += 'app_key=' + app_key
        _str = hashlib.md5(_str.encode('utf-8')).hexdigest()
        return _str.upper()
    except Exception as e:
        logger.error('tencen get_sign_code error [{}]'.format(e))

def asr(filename, rate=16000):
    with open(filename,'rb') as f:
        _byte = f.read()
    base64_audio = base64.b64encode(_byte)
    url = 'https://api.ai.qq.com/fcgi-bin/aai/aai_asr'
    ##    requests中data传入json字符串
    ##==================================
    ##    app_id        000001	应用标识（AppId）
    ##    time_stamp    请求时间戳（秒级）
    ##    nonce_str     随机字符串
    ##    sign          签名信息，详见接口鉴权
    ##    format        语音压缩格式编码，定义见下文描述
    ##    speech	待识别语音（时长上限30s）长度上限8MB
    ##    rate          16000	语音采样率编码 默认即16KHz
    params = {'app_id'      : config.tengxun.APP_ID,
              'time_stamp'  : int(time.time()),
              'nonce_str'   : '12532153215321',
              'format'      : 2,
              'speech'      : base64_audio.decode(),
              'rate'        : 8000,
              'sign'        :''}
    sign = get_sign_code(params, config.tengxun.API_KEY)
    params['sign'] = sign
    rt = requests.post(url, data=params)
    jsonData = json.loads(rt.text)
    if jsonData.get('ret') == 0:
        return True,jsonData.get('data').get('text')
    else:
        return False,rt.text

if __name__ == "__main__":
    t,s = asr('../file4easy_test/白天喜欢吃白菜.wav')
    print(s)
