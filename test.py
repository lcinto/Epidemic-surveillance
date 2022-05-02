import requests
from bs4 import BeautifulSoup as Bs

response = requests.get("https://www.douyu.com/directory/all")
# print(response.text)

html = response.text
html_tree = Bs(html, "html.parser")
print(html_tree)
