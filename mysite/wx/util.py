
class dealtext(FromUserName,access_token):
    """docstring for """
    def __init__(self, FromUserName,access_token):
        self.FromUserName = FromUserName
        self.access_token = access_token

    def getrequest(self):
        data={}
        url_parame=urllib.parse.urlencode(data)
        url="https://api.weixin.qq.com/cgi-bin/user/info?access_token="+self.access_token+"&openid="+self.FromUserName+"&lang=zh_CN"
        all_url=url+url_parame
        data=urllib.request.urlopen(all_url).read()
        print(data)
        print('-------------------------------')
        record=json.loads(data.decode('UTF-8')) 
        print(record)
        