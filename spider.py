import requests
import pymysql
import time, datetime
import json
import hashlib
import traceback
import sys
from bs4 import BeautifulSoup
import re

def get_tencent_data():
    """
    :return: 返回历史数据和当日详细数据
    """
    url_det = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf'
    url_his = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
    }
    r_det = requests.get(url_det, headers)
    r_his = requests.get(url_his, headers)
    res_det = json.loads(r_det.text)  # json字符串转字典
    res_his = json.loads(r_his.text)
    data_det = res_det['data']['diseaseh5Shelf']
    data_his = res_his['data']

    history = {}  # 历史数据
    for i in data_his["chinaDayList"]:
        if (i["date"] > "04.01"):
            ds = i["y"] + "." + i["date"]
            tup = time.strptime(ds, "%Y.%m.%d")
            ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型
            confirm = i["confirm"]
            confirm_now = i["nowConfirm"]
            suspect = i["suspect"]
            heal = i["heal"]
            dead = i["dead"]
            history[ds] = {"confirm": confirm, "confirm_now": confirm_now, "suspect": suspect, "heal": heal,
                           "dead": dead}
        else:
            continue
    for i in data_his["chinaDayAddList"]:
        if (i["date"] > "04.01"):
            ds = i["y"] + "." + i["date"]
            tup = time.strptime(ds, "%Y.%m.%d")
            ds = time.strftime("%Y-%m-%d", tup)
            confirm_add = i["confirm"]
            suspect_add = i["suspect"]
            heal_add = i["heal"]
            dead_add = i["dead"]
            history[ds].update(
                {"confirm_add": confirm_add, "suspect_add": suspect_add, "heal_add": heal_add, "dead_add": dead_add})
        else:
            continue

    details = []  # 当日详细数据
    update_time = data_det["lastUpdateTime"]
    data_country = data_det["areaTree"]  # list 之前有25个国家,现在只有中国
    print(data_country)
    data_province = data_country[0]["children"]  # 中国各省
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]  # 城市名
            confirm = city_infos["total"]["confirm"]  # l累计确诊
            confirm_add = city_infos["today"]["confirm"]  # 新增确诊
            confirm_now = city_infos["total"]["nowConfirm"]  # 现有确诊
            heal = city_infos["total"]["heal"]  # 累计治愈
            dead = city_infos["total"]["dead"]  # 累计死亡
            details.append([update_time, province, city, confirm, confirm_add, confirm_now, heal, dead])
    return history, details


get_tencent_data()
# print(get_tencent_data())
