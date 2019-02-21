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
#from .util import getrequest 
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
    data = Wx_Access_Token.objects.all().last()
    access_token = data.access_token
    url = request.get_full_path()
    print('##############')
    print(url)
    print('##############')
    try:
        webData = request.body
        xmlData = ET.fromstring(webData)
        msg_type = xmlData.find('MsgType').text
        ToUserName = xmlData.find('ToUserName').text
        FromUserName = xmlData.find('FromUserName').text
        CreateTime = xmlData.find('CreateTime').text
        MsgType = xmlData.find('MsgType').text
        MsgId = xmlData.find('MsgId').text
        Content = xmlData.find('Content').text

        toUser = FromUserName
        fromUser = ToUserName
        #请求用户个人信息----------------
        data={}
        url_parame=urllib.parse.urlencode(data)
        url="https://api.weixin.qq.com/cgi-bin/user/info?access_token="+access_token+"&openid="+fromUser+"&lang=zh_CN"
        all_url=url+url_parame
        data=urllib.request.urlopen(all_url).read()
        print(data)
        print('-------------------------------')
        record=json.loads(data.decode('UTF-8')) 
        print(record)
        #请求用户个人信息----------------
        if msg_type == 'text':
            if Content not in (1,2):
                content = "你要接受心理测试么？\n 1.是 \n 2.否"
                if Content == '1':
                    content = '好'
                if Content == '2':
                    content ='不好'
            replyMsg = TextMsg(toUser, fromUser, content)

            return replyMsg.send()

    except Exception as e:
        return e

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

