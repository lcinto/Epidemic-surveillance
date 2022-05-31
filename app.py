from flask import Flask, request, render_template, jsonify
from jieba.analyse import extract_tags
import string
import utils

import requests
import pymysql
import time
import json
import hashlib
import traceback
import sys
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data:
        day.append(a.strftime("%m-%d"))  # a是datatime类型
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    # end_update_time, province, city, county, address, type
    details = []
    risk = []
    end_update_time = data[0][0]
    for a, b, c, d, e, f in data:
        risk.append(f)
        details.append(f"{b}\t{c}\t{d}\t{e}")
    return jsonify({"update_time": end_update_time, "details": details, "risk": risk})


@app.route("/c1")
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm": int(data[0]), "confirm_now": int(data[1]), "heal": int(data[2]), "dead": int(data[3])})


@app.route("/c2")
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        # [{'name': '上海', 'value': 318}, {'name': '云南', 'value': 162}]
        res.append({"name": tup[0], "value": int(tup[1])})
    #print(res)
    return jsonify({"data": res})


@app.route("/r1")
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k, v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


@app.route("/r2")
def get_r2_data():
    data = utils.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)  # 移除热搜数字
        v = i[0][len(k):]  # 获取热搜数字
        ks = extract_tags(k)  # 使用jieba 提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})


@app.route('/')
def main():
    return render_template("main.html")
#################
@app.route('/main2')
def hello_world():
    return render_template("main2.html")

@app.route("/left1")
def get_left_data():
    res = []
    for tup in utils.get_left_data():  # ((国家)(确诊)(死亡))
        # [{'name': '上海', 'value': 318}, {'name': '云南', 'value': 162}]
        res.append({"name": tup[0], "value": int(tup[1])})
    #print(res)
    return jsonify({"data": res})

@app.route("/left2")
def get_rose_data():
    res = []
    for tup in utils.get_left_data():  # ((国家)(确诊)(死亡))
        #res格式 [{'name': '云南', 'confirm': 162,'dead':10}]
        res.append({"name": tup[0], "confirm": int(tup[1]),"dead":int(tup[2])})
    #(res)
    return jsonify({"data": res})

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

def get_tencent_data():
    """
    :return: 返回历史数据和当日详细数据
    """
    url_det = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=diseaseh5Shelf'
    url_his = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList," \
              "chinaDayAddList,nowConfirmStatis,provinceCompare "
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
    }
    r_det = requests.get(url_det, headers)
    r_his = requests.get(url_his, headers)
    res_det = json.loads(r_det.text)  # json字符串转字典
    res_his = json.loads(r_his.text)
    # print(r_det.text)
    data_det = res_det['data']['diseaseh5Shelf']
    data_his = res_his['data']
    # print(data_det)
    history = {}  # 历史数据
    for i in data_his["chinaDayList"]:
        if i["date"] > "04.01":
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
        if i["date"] > "04.01":
            ds = i["y"] + "." + i["date"]
            tup = time.strptime(ds, "%Y.%m.%d")
            ds = time.strftime("%Y-%m-%d", tup)
            confirm_add = i["confirm"]
            suspect_add = i["suspect"]
            heal_add = i["heal"]
            dead_add = i["dead"]
            history[ds].update(
                {"confirm_add": confirm_add, "suspect_add": suspect_add, "heal_add": heal_add,
                 "dead_add": dead_add})
        else:
            continue

    details = []  # 当日详细数据
    update_time = data_det["lastUpdateTime"]
    data_country = data_det["areaTree"]  # list 之前有25个国家,现在只有中国
    # print(data_country)
    data_province = data_country[0]["children"]  # 中国各省
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]  # 城市名
            confirm = city_infos["total"]["confirm"]  # 累计确诊
            confirm_add = city_infos["today"]["confirm"]  # 新增确诊
            confirm_now = city_infos["total"]["nowConfirm"]  # 现有确诊
            heal = city_infos["total"]["heal"]  # 累计治愈
            dead = city_infos["total"]["dead"]  # 累计死亡
            details.append([update_time, province, city, confirm, confirm_add, confirm_now, heal, dead])
            # 更新时间，省，城市，确诊病例，确诊新增，现存确诊，治愈，死亡病例
    return history, details

def get_baidu_hot():
    """
    :return: 返回百度疫情热搜
    """
    # url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, features="html.parser")
    kw = soup.select("div.c-single-text-ellipsis")
    count = soup.select("div.hot-index_1Bl1a")
    context = []
    for i in range(len(kw)):
        k = kw[i].text.strip()  # 移除左右空格
        v = count[i].text.strip()
        # print(f"{k}{v}".replace('\n',''))
        context.append(f"{k}{v}".replace('\n', ''))
    return context

def get_risk_area():
    """
    :return: risk_h,risk_m 中高风险地区详细数据
    """
    # 当前时间戳
    o = '%.3f' % (time.time() / 1e3)
    e = o.replace('.', '')
    i = "23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA"
    a = "123456789abcdefg"
    # 签名1
    s1 = hashlib.sha256()
    s1.update(str(e + i + a + e).encode("utf8"))
    s1 = s1.hexdigest().upper()
    # 签名2
    s2 = hashlib.sha256()
    s2.update(str(e + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA' + e).encode("utf8"))
    s2 = s2.hexdigest().upper()
    # post请求数据
    post_dict = {
        'appId': 'NcApplication',
        'key': '3C502C97ABDA40D0A60FBEE50FAAD1DA',
        'nonceHeader': '123456789abcdefg',
        'paasHeader': 'zdww',
        'signatureHeader': s1,
        'timestampHeader': e
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Referer': 'http://bmfw.www.gov.cn/',
        'Origin': 'http://bmfw.www.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36',
        'x-wif-nonce': 'QkjjtiLM2dCratiA',
        'x-wif-paasid': 'smt-application',
        'x-wif-signature': s2,
        'x-wif-timestamp': e,
    }
    url = "http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson"
    req = requests.post(url=url, data=json.dumps(post_dict), headers=headers)
    resp = req.text
    res = json.loads(resp)
    # print(res)
    utime = res['data']['end_update_time']  # 更新时间
    hcount = res['data'].get('hcount', 0)  # 高风险地区个数
    mcount = res['data'].get('mcount', 0)  # 低风险地区个数
    # 具体数据
    hlist = res['data']['highlist']
    mlist = res['data']['middlelist']

    risk_h = []
    risk_m = []

    for hd in hlist:
        type = "高风险"
        province = hd['province']
        city = hd['city']
        county = hd['county']
        area_name = hd['area_name']
        communitys = hd['communitys']
        for x in communitys:
            risk_h.append([utime, province, city, county, x, type])

    for md in mlist:
        type = "中风险"
        province = md['province']
        city = md['city']
        county = md['county']
        area_name = md['area_name']
        communitys = md['communitys']
        for x in communitys:
            risk_m.append([utime, province, city, county, x, type])

    return risk_h, risk_m

def update_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  # 0 是历史数据字典,1 最新详细数据列表
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,confirm_now,heal,dead) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)'  # 对比当前最大时间戳
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:  # 判断数据是否是历史数据，如果不是，执行数据更新，
            print(f"{time.asctime()}开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0 是历史数据字典,1 最新详细数据列表
        print(f"{time.asctime()}开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, k):  # 如果当天数据不存在，才写入
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("confirm_now"),
                                     v.get("suspect"), v.get("suspect_add"), v.get("heal"),
                                     v.get("heal_add"), v.get("dead"), v.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_hotsearch():
    """
    将疫情热搜插入数据库
    :return:
    """
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))  # 插入数据
        conn.commit()  # 提交事务保存数据
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def update_risk_area():
    """
        更新 risk_area 表
        :return:
        """
    cursor = None
    conn = None
    try:
        risk_h, risk_m = get_risk_area()
        conn, cursor = get_conn()
        sql = "insert into risk_area(end_update_time,province,city,county,address,type) values(%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select end_update_time from risk_area order by id desc limit 1)'  # 对比当前最大时间戳
        cursor.execute(sql_query, risk_h[0][0])  # 传入最新时间戳
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in risk_h:
                cursor.execute(sql, item)
            for item in risk_m:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

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
            cursor.execute(sql, [context[i].get('name'), context[i].get('confirm'), context[i].get('dead')])  # 插入数据
        conn.commit()  # 提交事务保存数据
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

@app.route("/all_data")
def get_all_data():

    update_history()
    update_details()
    update_hotsearch()
    update_risk_area()
    update_worlddata()
    return jsonify({"data": 'ok'})


app.run(host="0.0.0.0", port=9999)
