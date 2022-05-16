from flask import Flask, request, render_template, jsonify
from jieba.analyse import extract_tags
import string
import utils

app2 = Flask(__name__)

@app2.route('/')
def hello_world():
    return render_template("index2.html")

@app2.route("/left1")
def get_left_data():
    res = []
    for tup in utils.get_left_data():  # ((国家)(确诊)(死亡))
        # [{'name': '上海', 'value': 318}, {'name': '云南', 'value': 162}]
        res.append({"name": tup[0], "value": int(tup[1])})
    print(res)
    return jsonify({"data": res})

@app2.route("/left2")
def get_rose_data():
    res = []
    for tup in utils.get_left_data():  # ((国家)(确诊)(死亡))
        #res格式 [{'name': '云南', 'confirm': 162,'dead':10}]
        res.append({"name": tup[0], "confirm": int(tup[1]),"dead":int(tup[2])})
    print(res)
    return jsonify({"data": res})

app2.run(host="0.0.0.0", port=9992)