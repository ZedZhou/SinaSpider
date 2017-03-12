import json
import base64
import requests

myWeibo = [
    {'user': '你的微博账号', 'psw': '密码'},
]

def getCookies(weibo):
    cookies = []  # cookie池
    loginUrl = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for item in weibo:
        account = item['user']
        password = item['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
            'entry': 'sso',
            'gateway': '1',
        'from': 'null',
        'savestate': '30',
        'useticket': '0',
        'pagerefer':'',
        'vsnf':'1',
        'su': username,
        'service':'sso',
        'sp': password,
        'sr': '1680 * 1050',
        'encoding': 'UTF-8',
        'domain': 'sina.com.cn',
        'prelt': '98',
        'returntype': 'TEXT',
        }

        sesseion = requests.Session()
        r = sesseion.post(loginUrl, data=postData)
        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        print(info)
        if info['retcode'] == '0':
            print('获取Cookie成功(Account: %s)' % account)
            cookie = sesseion.cookies.get_dict()
            cookies.append(cookie)
        else:
            print('Failed! Reason:%s' % info['reason'])
    return cookies
# print(base64.b64encode('47662321@qq.com'.encode('utf-8')).decode('utf-8'))

cookies = getCookies(myWeibo)
print(cookies)

