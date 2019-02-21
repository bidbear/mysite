def getrequest(toUser,access_token):
        data={}
        url_parame=urllib.parse.urlencode(data)
        url="https://api.weixin.qq.com/cgi-bin/user/info?access_token="+access_token+"&openid="+toUser+"&lang=zh_CN"
        all_url=url+url_parame
        data=urllib.request.urlopen(all_url).read()
        print(data)
        print('-------------------------------')
        record=json.loads(data.decode('UTF-8')) 
        print(record)
        return 123
        