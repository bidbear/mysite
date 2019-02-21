import urllib
import urllib.request
from .models import Wx_Access_Token
import json
from django.http import HttpResponse
from django.shortcuts import render
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
#获取token
def index(request):
    content={}
    content['token']=Wx_Access_Token.objects.all().last()

    return render(request,'index.html',content)
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
