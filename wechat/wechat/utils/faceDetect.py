#!/usr/bin/env python
# coding: utf-8

import hashlib
import time
import random
import string
import requests
from urllib.parse import quote
import base64
from urllib.parse import urlencode
import os
from .config import *

def calcMD5(content):
    m = hashlib.md5(content.encode())
    return m.hexdigest().upper()



def getParams(imgData):
    global params
    #请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp=str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    # 应用标志，这里修改成自己的id和key  
    # app_id='2130028959'
    # app_key='KgV0yKu1CkX2GoEi'
    params = {'app_id':appID_faceDetect_TX,
              'image':imgData,
              'time_stamp':time_stamp,
              'nonce_str':nonce_str,
              'mode':'1'
             }
    #要对key排序再拼接
    paramsSorted = sorted(params.items(), key=lambda item:item[0], reverse = False)
    paramsSorted.append(('app_key',appKey_faceDetect_TX))
    rawParams= urlencode(paramsSorted)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = calcMD5(rawParams)
    params['sign'] = sign
    return params




def get_result(imgPath):
    global payload,r
    # 聊天的API地址  
    url = "https://api.ai.qq.com/fcgi-bin/face/face_detectface"
    # 获取请求参数 
    with open(imgPath,'rb') as f:
        imgData = base64.b64encode(f.read())  
    payload = getParams(imgData)
    # r = requests.get(url,params=payload)  
    r = requests.post(url,data=payload)
    return r.json()
#     return r.json()["data"]["answer"]





def imgDownload(imgUrl, name):
    """
    下载微信发送过来的图片
    imgUrl:图片的网址
    """
    r = requests.get(imgUrl)
    imgName = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    path = os.path.abspath('.')
    with open('images/{}.jpg'.format(imgName), 'wb') as f:
        f.write(r.content)
    if os.path.getsize(fd.name) >= 1048576:
        return 'large'
    # print('namename', os.path.basename(fd.name))
    return os.path.basename(fd.name)



def numTranslate(dataJson):
    if dataJson['glass'] == 1:  # 眼镜
        glass = '眼镜：有'
    else:
        glass = '眼镜：无'
    if dataJson['gender'] >= 70:  # 性别值从0-100表示从女性到男性
        gender = '性别：男'
    elif 50 <= dataJson['gender'] < 70:
        gender = "性别：娘"
    elif dataJson['gender'] < 30:
        gender = '性别：女'
    else:
        gender = '性别：女汉子'
    if 90 < dataJson['expression'] <= 100:  # 表情从0-100，表示笑的程度
        expression = '表情：一笑倾城'
    elif 80 < dataJson['expression'] <= 90:
        expression = '表情：心花怒放'
    elif 70 < dataJson['expression'] <= 80:
        expression = '表情：兴高采烈'
    elif 60 < dataJson['expression'] <= 70:
        expression = '表情：眉开眼笑'
    elif 50 < dataJson['expression'] <= 60:
        expression = '表情：喜上眉梢'
    elif 40 < dataJson['expression'] <= 50:
        expression = '表情：喜气洋洋'
    elif 30 < dataJson['expression'] <= 40:
        expression = '表情：笑逐颜开'
    elif 20 < dataJson['expression'] <= 30:
        expression = '表情：似笑非笑'
    elif 10 < dataJson['expression'] <= 20:
        expression = '表情：半嗔半喜'
    elif 0 <= dataJson['expression'] <= 10:
        expression = '表情：黯然伤神'
    beauty = '魅力：' + str(dataJson['beauty'])
    age = '年龄：' + str(dataJson['age'])
    result = '\n'.join([gender, age, expression, beauty, glass])
    return result

def getResultFromUrl(testPicUrl):
    global payload,r
    r = requests.get(testPicUrl)
    imgData = base64.b64encode(r.content)  
    payload = getParams(imgData)
    url = "https://api.ai.qq.com/fcgi-bin/face/face_detectface"
    r = requests.post(url,data=payload)
    # result = numTranslate(r.json()['data']['face_list'][0])
    # return result
    return r.json()





