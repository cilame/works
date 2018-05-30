import requests
import datetime
from hashlib import md5,sha1
from base64 import b64encode
import hmac, json, sys

from .config import aliyun

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

def get_signature(content,
                  method,
                  content_type,
                  accept,
                  date,
                  data_len):
    bodymd5  = b64encode(md5(content).digest())
    md52str  = b64encode(md5(bodymd5).digest()).decode()
    str2sign = method+"\n"+accept+"\n"+md52str+"\n"+content_type+"\n"+date
    signature = hmac.new(aliyun.ACCESSKEY_SECRET.encode(),
                         str2sign.encode(),
                         sha1).digest()
    return b64encode(signature).decode()

def asr(filename,rate=8000,raw="wav",model="customer-service-8k"):
    
    #TODO assert model (eg."customer-service-8k") match rate (eg.8000)
    url = "https://nlsapi.aliyun.com/recognize?version=2.0&"
    if rate == 8000:
        url += "appkey=nls-service-8k&"
    if rate == 16000:
        model = "customer-service"
    url = url + "model=" + model
    ##    model
    ##=====================================
    ##    customer-service-8k	中文	8KHz	客服对话
    ##    customer-service	中文	16KHz	客服对话
    ##    chat	中文	16KHz	社交聊天
    ##    entertainment	中文	16KHz	家庭娱乐
    ##    shopping	中文	16KHz	电商购物
    ##    english	英文	16KHz	英文转写

    with open(filename,'rb') as f:
        content = f.read()

    method       = "POST"
    content_type = "audio/%s; samplerate=%d"%(raw,rate)
    accept       = "application/json"
    date         = datetime.datetime.utcnow().strftime(GMT_FORMAT)
    data_len     = "%d"%len(content)
    #TODO assert content len < 2M?

    accesskey_id = aliyun.ACCESSKEY_ID
    signature    = get_signature(content,
                                 method,
                                 content_type,
                                 accept,
                                 date,
                                 data_len)

    authorization = "Dataplus %s:%s"%(accesskey_id,signature)
    headers = {
        "User-Agent"    : "Mozilla/5.0 (Windows NT 6.1)",
        "Authorization" : authorization,
        "Content-type"  : content_type,
        "Accept"        : accept,
        "Date"          : date,
        "Content-Length": data_len,
    }
    req = requests.post(url, data=content, headers=headers)
    result = json.loads(req.text).get("result")
    if result:
        return True,result
    else:
        return False,req.text

if __name__ == "__main__":
    s = asr('../file4test/c7678235123242079a7c7658b478bd46.wav',rate=8000)
    print(s)

