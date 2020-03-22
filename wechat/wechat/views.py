from wechatpy.utils import check_signature
from . import settings
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import parse_message, create_reply
from wechatpy.replies import BaseReply
from wechatpy import WeChatClient
from wechatpy.oauth import WeChatOAuth
from wechatpy.replies import TextReply
from django.shortcuts import redirect

# from .utils import youdaoTranslate
from .utils.google_translate import googleTranslate
from .utils.CasualChat_tencent import getAns
from .utils.faceDetect import getResultFromUrl, numTranslate
# import wx.wechat as wx_wechat


# 连接微信公众号的方法
def serve(request):
    # GET 方式用于微信公众平台绑定验证
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(settings.Token, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求'
        response = HttpResponse(echo_str)
    else:

        msg = parse_message(request.body)
        msg_dict = msg.__dict__['_data']
        # print(msg.id, msg.source, msg.create_time, msg.type, msg.target, msg.time, msg.__dict__['_data']['Event'], '====')
        if msg.type == 'text':
            print(msg)
            # print(msg.source)
            # print(msg.target)
            # transResult = youdaoTranslate(msg.content)
            # transResult = googleTranslate(msg.content)
            transResult = getAns(msg.content)
            transResult = transResult if transResult != '' else '我好像不明白'
            reply = TextReply(content= transResult, messsage=msg)
            reply.source = msg.target
            reply.target = msg.source
            xml = reply.render()
            print(reply)
            # pass
        elif msg.type == 'event':
            if msg_dict['Event'] == 'subscribe':
                    # 关注后 将获取的用户的信息保存到数据库
                # wx_wechat.subscribe(getWxUserInfo(msg.source))
                print('subscribe')
            elif msg_dict['Event'] == 'unsubscribe':
                    # 取关后，将用户的关注状态更改为 未关注
                # wx_wechat.unsubscribe(msg.source)
                print('subscribe')
        elif msg.type == 'image':
            print(msg)
            faceResult = getResultFromUrl(msg.image)
            if faceResult['ret']!=0:
                reply = TextReply(content= '未检测到人脸', messsage=msg)
            else:
                content = numTranslate(faceResult['data']['face_list'][0])
                reply = TextReply(content= content, messsage=msg)
            reply.source = msg.target
            reply.target = msg.source
            xml = reply.render()
        else:
            pass
        response = HttpResponse(xml, content_type="application/xml")
    return response


def getWxClient():
    return WeChatClient(settings.AppID, settings.AppSecret)


def getWxUserInfo(openid):
    wxClient = getWxClient()
    wxUserInfo = wxClient.user.get(openid)
    return wxUserInfo


def getWeChatOAuth(redirect_url):
    return WeChatOAuth(settings.AppID, settings.AppSecret, redirect_url)

# 定义授权装饰器
def oauth(method):
    def warpper(request):
        if request.session.get('user_info', None) is None:
            code = request.GET.get('code', None)
            wechat_oauth = getWeChatOAuth(request.get_raw_uri())
            url = wechat_oauth.authorize_url
            if code:
                try:
                    wechat_oauth.fetch_access_token(code)
                    user_info = wechat_oauth.get_user_info()
                except Exception as e:
                    print(str(e))
                    # 这里需要处理请求里包含的 code 无效的情况
                    # abort(403)
                else:
                    request.session['user_info'] = user_info
            else:
                return redirect(url)

        return method(request)
    return warpper

@oauth
def get_wx_user_info(request):
    user_info = request.session.get('user_info')
    return HttpResponse(str(user_info))