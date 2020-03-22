#公众号utils

from urllib.parse import quote
from urllib.request import urlopen
import json

def youdaoTranslate(words):
	"""
	利用有道api进行翻译
	params:
		words:待翻译的句子
	return:
		ans：翻译结果
	"""
	qword = quote(words)
	baseurl =r'http://fanyi.youdao.com/openapi.do?keyfrom=hitonystark&key=2023711410&type=data&doctype=json&version=1.1&q='
	targetUrl = baseurl+qword
	resp = urlopen(targetUrl)
	trans = json.loads(resp.read())
	if trans['errorCode'] == 0:        
	    ans =''.join(trans['translation'])
	    return ans
	return 'translation false'