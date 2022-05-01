from urllib import request

'''
url = "http://www.baidu.com"
res = request.urlopen(url)  # 获取响应

# print(res.info())  # 响应头
# print(res.getcode())  # 获取状态码
# print(res.geturl())  # 返回响应

html = res.read()
# print(html)
html = html.decode('utf-8')
print(html)
'''
url = "http://www.dianping.com"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32 '
}
req = request.Request(url, headers=header)
res = request.urlopen(req)  # 获取响应

print(res.info())  # 响应头
print(res.getcode())  # 获取状态码
print(res.geturl())  # 返回响应

html = res.read()
# print(html)
html = html.decode('utf-8')
print(html)
