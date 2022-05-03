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

time_str = time.strftime("%Y{}%m{}%d{} %X")

print(time_str.format("年", "月", "日"))
# print(get_risk_area())
