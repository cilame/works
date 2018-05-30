# -*- coding: UTF-8 -*-
import time
import urllib
import requests
import json
from base64 import b64encode
import hmac

import config

SECRETID  = config.tengxunyun.SECRETID
SECRETKEY = config.tengxunyun.SECRETKEY

# 目前硬编 SourceType 为 1
# 即上传文件模式
def asr(filename,rate=16000):
    #==================#
    #    start init    #
    #==================#
    query_arr = {}
    query_arr['Action']         = 'SentenceRecognition'
    query_arr['SecretId']       = SECRETID
    query_arr['Timestamp']      = int(time.time())
    query_arr['Nonce']          = str(query_arr["Timestamp"])[0:4]
    query_arr['Version']        = '2018-05-22'
    query_arr['ProjectId']      = 0
    query_arr['SubServiceType'] = 2
    if rate == 16000: query_arr['EngSerViceType'] = '16k'  # 用户填写，分为16k和8k，目前8k仅测试使用
    if rate == 8000 : query_arr['EngSerViceType'] = '8k'
    query_arr['SourceType']     = 1

    with open(filename,'rb') as f:
        content = f.read()
    data = b64encode(content).decode()
    query_arr["Data"]           =data
    query_arr["DataLen"]        =len(data)
    query_arr['VoiceFormat']    = 'wav'                 # 用户填写，现在支持MP3和wav
    query_arr['UsrAudioKey']    = 'c2hlbnpoaQ==00000001'# 用户填写，语音文件的唯一标识

    host = 'aai.tencentcloudapi.com'
    uri = '/'
    tempArray = []
    for key in sorted(query_arr):
        strs = key.replace("_",".") + "=" + str(query_arr[key])
        tempArray.append(strs)
    strParam = "&".join(tempArray)
    signStr  = "POST" + host + uri + "?" + strParam

    sign = b64encode(hmac.new(SECRETKEY.encode(),signStr.encode(),"sha1").digest()).decode()

    query_arr["Signature"] = sign
    #==================#
    #   init finish    #
    #==================#
    url='https://aai.tencentcloudapi.com'
    headers = {
        "Host":"aai.tencentcloudapi.com",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"
    }
    v = requests.post(url,data=query_arr,headers=headers)
    if v.status_code == 200:
        rdata = json.loads(v.text)
        voice = rdata.get("Response").get("Result")
        error = rdata.get("Response").get("Error")
        print(True, str(v.status_code) +' '+ str(v.text))       #debug
        if voice:
            return True, voice
        elif error:
            return False, str(v.status_code) +' '+ str(v.text)
        else:
            return False, str(v.status_code) +' '+ str(v.text)
    else:
        print(False, str(v.status_code) +' '+ str(v.text))      #debug
        return False,str(v.status_code) +' '+ str(v.text)

if __name__ == "__main__":
    filename  = '../file4easy_test/音频文件1526795927005.wav'
    for i in range(10):
        status,voice = asr(filename,rate=16000)
        print(voice)
        
