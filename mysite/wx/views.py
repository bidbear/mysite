import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

#django默认开启csrf防护，这里使用@csrf_exempt去掉防护    
@csrf_exempt
def wx(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')
        print(signature)
        #服务器配置中的token
        token = 'X4v0VI1NnwoN00WdqvqjS46sw3bsVdQp'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')
        hashstr = hashlib.sha1(hashstr).hexdigest()
        print(hashstr)
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        autoreply(request)
        return HttpResponse('error')
def autoreply(request):
    pass