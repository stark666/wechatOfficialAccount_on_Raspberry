#!/usr/bin/env python
# coding: utf-8

# In[5]:


import hashlib
import time
import random
import string
import requests
from urllib.parse import quote
from .config import *

# In[3]:


def calcMD5(content):
    m = hashlib.md5(content.encode('UTF-8'))
    return m.hexdigest().upper()


# In[17]:


def getParams(plus_item):
    global params
    #请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp=str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key  
    app_id = appID_CasualChat_TX
    app_key = appKey_CasualChat_TX
    params = {'app_id':app_id,
              'question':plus_item,
              'time_stamp':time_stamp,
              'nonce_str':nonce_str,
              'session':'10000'
             }
    signBefore = ''
    #要对key排序再拼接
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。
        signBefore += '{}={}&'.format(key,quote(params[key], safe=''))
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾
    signBefore += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = calcMD5(signBefore)
    params['sign'] = sign
    return params


# In[18]:


def getAns(plus_item):
    global payload,r
    # 聊天的API地址  
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数  
    plus_item = plus_item.encode('utf-8')
    payload = getParams(plus_item)
    # r = requests.get(url,params=payload)  
    r = requests.post(url,data=payload)
    # return r.json()
    return r.json()["data"]["answer"]


# In[21]:

if __name__ == '__main__':
    ques = '你是谁'
    ans = getAns(ques)
    print(ans)

# In[22]:




# In[ ]:




