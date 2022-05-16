from flask import Flask, request, render_template, jsonify
from jieba.analyse import extract_tags
import string
import utils
import time
import pymysql

print(utils.get_worldmap_data())
