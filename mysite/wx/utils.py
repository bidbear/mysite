from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '15604010'
API_KEY = '380mDqOGDNONoPmieEYeL4ak'
SECRET_KEY = 'F8DeFtQvkheZWXN3l2kTRysN0DsUKC7F'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def Toword(picurl):
    url = picurl

    """ 调用网络图片文字识别, 图片参数为远程url图片 """
    client.webImageUrl(url);
    """ 如果有可选参数 """
    options = {}
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    """ 带参数调用网络图片文字识别, 图片参数为远程url图片 """
    result = client.webImageUrl(url, options)
    for content in result['words_result']:
        return content['words']