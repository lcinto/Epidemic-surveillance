import requests
from bs4 import BeautifulSoup

# url="http://www.dianping.com"
# header={
#
# }
# res=requests.get(url)
#
# print(res.info())
# print(res.getcode())
# print(res.geturl())
#
# html=res.read()
# print(html.decode("utf-8"))
#
#
# print(res.status_code)

# url = "http://wsjkw.sc.gov.cn/scwsjkw/gzbd/fyzt.shtml"
# res = requests.get(url)
# res.encoding = "utf-8"
# html = res.text
# soup = BeautifulSoup(html,'lxml')
# print(soup.find("h2").text)
# a=soup.find("a")
# print(a.attrs["href"])
# url_new="http://wsjkw.sc.gov.cn"+a.attrs["href"]
# res=requests.get(url_new)
# res.encoding="utf-8"
# soup=BeautifulSoup(res.text,'lxml')
# context=soup.find(style="font-size: 12pt;")
# print(context)

