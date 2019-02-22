from aip import AipOcr
import urllib
import ssl
import json
import requests
from PIL import Image
from io import BytesIO
""" 你的 APPID AK SK """
APP_ID = '15604010'
API_KEY = '380mDqOGDNONoPmieEYeL4ak'
SECRET_KEY = 'F8DeFtQvkheZWXN3l2kTRysN0DsUKC7F'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

#----------------------------------------------------------------------------------------------------------------
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
#定义list获取文字列表
    contents=[]
    str=''
    for content in result['words_result']:
         contents.append(content['words'])
#返回文字的列表字符串
    print(contents)
    return str.join(contents) 
#----------------------------------------------------------------------------------------------------------------
""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
# 获取身份证正面信息
def getidCard():
    image = get_file_content('/data/wwwroot/mysite/mysite/static/idCard/123.jpg')
    idCardSide = "front"

    """ 调用身份证识别 """
    client.idcard(image, idCardSide);

    """ 如果有可选参数 """
    options = {}
    options["detect_direction"] = "true"
    options["detect_risk"] = "false"

    """ 带参数调用身份证识别 """
    result = client.idcard(image, idCardSide, options)
    list =[]
    str ='\n'
    for key,values in  result['words_result'].items():
        list.append('%s : %s ' % (key,values['words']))
    if len(list) < 6:
        return '请上传正确的身份证图片'
    else:
        return str.join(list)
#--------------保存图片-----------------------------------------------------------------------------------

def SaveImg(picurl):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK 
    img_src = picurl
    response = requests.get(img_src)
    image = Image.open(BytesIO(response.content))
    image.save('/data/wwwroot/mysite/mysite/static/idCard/123.jpg')
    print('保存成功')
    return getidCard()