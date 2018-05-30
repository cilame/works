import os, sys
from aip import AipSpeech

import config

client = None

def asr(filename,rate=16000):
    '''
    使用使用百度语音识别需要先调用AipSpeech生成小服务
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    '''
    APP_ID = config.baiduyun.APP_ID
    API_KEY = config.baiduyun.API_KEY
    SECRET_KEY = config.baiduyun.SECRET_KEY

    global client
    if not client:
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    with open(filename,'rb') as f:
        content =  f.read()
    
    req = client.asr(
        content,
        format="wav",
        rate=rate,
        options={'dev_pid':1537} # 普通话
        )
    result = req.get("result")
    if result:
        return True,''.join(result)
    else:
        return False,req

if __name__ == "__main__":
    # 4 test
    filename = '../file4easy_test/c7678235123242079a7c7658b478bd46.wav'
    print(asr(filename,8000))
