import requests
import pymysql
import time
import datetime
import json
import hashlib
import traceback
import sys
from bs4 import BeautifulSoup
import re


def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                           user="root",
                           password="123456",
                           db="cov",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def get_world_data():
    """
    :return: 返回世界疫情数据
    """
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryConfirmAdd,WomWorld,WomAboard'
    url2 = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
    }
    res = requests.get(url, headers=headers)
    res2 = requests.get(url2, headers=headers)
    res_dict = json.loads(res.text)  # json字符串转字典
    res2_dict = json.loads(res2.text)
    res_data = res_dict['data']['WomAboard']
    res2_data = res2_dict['data']['diseaseh5Shelf']
    worlddata = {}
    for i in range(0, len(res_data) - 1):
        name = res_data[i]['name']
        confirm = res_data[i]['confirm']
        dead = res_data[i]['dead']
        worlddata[name] = {'name': name, 'confirm': confirm, 'dead': dead}
    worlddata['中国'] = {'name': '中国', 'confirm': res2_data['chinaTotal']['confirm'],
                       'dead': res2_data['chinaTotal']['dead']}
    # 例子worlddata={‘中国’：{'name': '中国', 'confirm': 1233, 'dead':123 }}
    return worlddata


def update_worlddata():
    cursor = None
    conn = None
    try:
        context = get_world_data()
        conn, cursor = get_conn()
        sql = "insert into world(country,confirm,dead) " \
              "values(%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
        for i, j in context.items():
            cursor.execute(sql,  [context[i].get('name'), context[i].get('confirm'), context[i].get('dead')])  # 插入数据
        conn.commit()  # 提交事务保存数据
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


update_worlddata()