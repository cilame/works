# -*- coding: utf-8 -*-
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.aai.v20180522 import aai_client, models

import time
from base64 import b64encode

from .config import tengxunyun
SECRETID = tengxunyun.SECRETID
SECRETKEY = tengxunyun.SECRETKEY

def asr(filename, rate=8000):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
        cred = credential.Credential(SECRETID, SECRETKEY)
        client = aai_client.AaiClient(cred, "ap-shanghai")
        with open(filename,'rb') as f:
            content = f.read()
        data = b64encode(content).decode()
        Timestamp = time.time()
        if rate == 16000: EngSerViceType = "16k"
        if rate ==  8000: EngSerViceType = "8k"
        params = {
            'ProjectId'      : 0,
            'SubServiceType' : 2,
            'EngSerViceType' : EngSerViceType,  # 用户填写，分为16k和8k，目前8k仅测试使用
            'SourceType'     : 1,
            'VoiceFormat'    : 'wav',           # 用户填写，现在支持MP3和wav
            'UsrAudioKey'    : 'c2hlbnpoaQ==00000001',
            'Data'           : data,
            'DataLen'        : len(data),
        }
        # 实例化一个请求对象
        req = models.SentenceRecognitionRequest()
        req._deserialize(params)
        resp = client.SentenceRecognition(req)
        return True,str(resp.to_json_string())
    except TencentCloudSDKException as err:
        return False,str(err)

if __name__ == "__main__":
    filename = './aaaaaa.wav'
    for i in range(30):
        v = asr(filename, 16000)
        print(i+1,v)
