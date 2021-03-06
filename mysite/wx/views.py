import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import urllib
import urllib.request
from gettoken.models import Wx_Access_Token
import xml.etree.ElementTree as ET
#导入处理百度api的模块
from .utils import Toword,SaveImg
#django默认开启csrf防护，这里使用@csrf_exempt去掉防护    
@csrf_exempt
def wx(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        #print(signature)
        #服务器配置中的token
        token = 'X4v0VI1NnwoN00WdqvqjS46sw3bsVdQp'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')
        hashstr = hashlib.sha1(hashstr).hexdigest()
        #print(hashstr)
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        #处理post请求
        othercontent = autoreply(request)
        return HttpResponse(othercontent)

# post请求处理
CONTENT=''
def autoreply(request):
    try:
        global CONTENT
        webData = request.body
        xmlData = ET.fromstring(webData)
        print(webData)
        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        #MsgId = xmlData.find('MsgId').text  
        toUser = FromUserName
        fromUser = ToUserName
        
        if msg_type == 'event':
            dy_event = xmlData.find('Event').text  
            print(dy_event)
            print('----------------------------------------------------------')
            if dy_event =='subscribe':
                content = "感谢订阅，目前公众号具有图片识别的功能，请不要频繁使用。。。。"
                replyMsg = TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                CONTENT=''
                content = "欢迎再次关注"
                replyMsg = TextMsg(toUser, fromUser, content)
                print(replyMsg.send())
        #用户发送消息判断
        if msg_type == 'text':
            Content = xmlData.find('Content').text
            if Content in ['1','文字','转文字','图转文','图片转文字']:
                CONTENT = '1'
                content = "请发送有文字的图片"
            elif Content in ['2','身份证','身份证照片转文字']:
                CONTENT = '2'
                content = "请发送身份证正面图片"     
            else:
                CONTENT = ''
                content = "我的现有功能如下，如果需要请输入相应的数字编号，或者文字：\n 1.图片转文字 \n 2.身份证照片转文字"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
    #转文字----------------------------------------------------
        elif msg_type == 'image':
            PicUrl = xmlData.find('PicUrl').text
            if CONTENT == '1':
                content = Toword(PicUrl)
            elif CONTENT == '2':
                content = SaveImg(PicUrl)
            else:
                content = '发送图片前，能不能问问我的意见'
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            content = "你到底 发的啥？"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception as e:
        replyMsg = TextMsg(toUser, fromUser, '数据错误')
        return replyMsg.send()

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        #self.MsgId = xmlData.find('MsgId').text

import time
class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
# --------------------- 
# 作者：Peace & Love 
# 来源：CSDN 
# 原文：https://blog.csdn.net/u013205877/article/details/77602853 
# 版权声明：本文为博主原创文章，转载请附上博文链接！


