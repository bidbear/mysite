import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import urllib
import urllib.request
from .models import Wx_Access_Token
#定时任务引用模块----------------------------------------------
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=5600)
def test_job():
    data={}
    url_parame=urllib.parse.urlencode(data)
    url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx32ed607e6951016c&secret=e65acf0f687135c8f953f26f52cdb2d0"
    all_url=url+url_parame
    data=urllib.request.urlopen(all_url).read()
    record=json.loads(data.decode('UTF-8'))
    print(record['access_token'])
    add_data=Wx_Access_Token(access_token = record['access_token'])
    add_data.save()
   
    # raise ValueError("Olala!")

register_events(scheduler)

scheduler.start()
print("Scheduler started!")

#定时任务引用模块----------------------------------------------

def index(request):
    content={}
    content['token']=Wx_Access_Token.objects.all().last()
    return render(request,'index.html',content)

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
    #get_(request)
import xml.etree.ElementTree as ET
def autoreply(request):
    try:
        webData = request.body
        print(webData)
        xmlData = ET.fromstring(webData)

        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text

        toUser = FromUserName
        fromUser = ToUserName

        if msg_type == 'text':
            content = "您好,欢迎来到Python大学习!希望我们可以一起进步!"
            replyMsg = TextMsg(toUser, fromUser, content)
            print "成功了!!!!!!!!!!!!!!!!!!!"
            print replyMsg
            return replyMsg.send()

        elif msg_type == 'image':
            content = "图片已收到,谢谢"
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
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = TextMsg(toUser, fromUser, content)
            return replyMsg.send()

    except Exception, Argment:
        return Argment

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

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
 #获取access_token 只需要运行一次       
def gettoken(request):
    data={}
    url_parame=urllib.parse.urlencode(data)
    url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx32ed607e6951016c&secret=e65acf0f687135c8f953f26f52cdb2d0"
    all_url=url+url_parame
    data=urllib.request.urlopen(all_url).read()
    record=json.loads(data.decode('UTF-8'))
    #print(record['access_token'])
    add_data=Wx_Access_Token(access_token = record['access_token'])
    add_data.save()
    str = '以获取最新的access_token'
    return HttpResponse(str)