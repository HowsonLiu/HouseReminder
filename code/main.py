# -*- coding:utf8 -*-
from EmailSender import EmailSender
from WebsiteAnjuke import *
import schedule
import configparser
import time

REFERSH_INTERVAL = 60
CONFIG_FILE_PATH = "./setup.cfg"
ACCOUNT = None
PASSWORD = None
OLD_URL = None

def check_and_send():
    global home_spider, OLD_URL, ACCOUNT, PASSWORD
    lastest_url = home_spider.get_first_url()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(lastest_url)
    if OLD_URL is not None and lastest_url is not None and lastest_url[:-20] == OLD_URL[:-20]:      # 除去url中的时间干扰
        return False
    detail_spider = DetailSpider(lastest_url)
    houseinfo = detail_spider.get_houseinfo()
    if houseinfo is None:
        print('Get Detail Error')
        return False
    sender = EmailSender()
    try:
        sender.login(ACCOUNT, PASSWORD)
        sender.send_house_info(houseinfo)
        OLD_URL = lastest_url
    except Exception as e:
        print('SMTP connected error: ' + repr(e))
        return False
    return True

def load_configure():
    global ACCOUNT, PASSWORD
    conf = configparser.ConfigParser()
    conf.read(CONFIG_FILE_PATH, encoding='utf-8')
    ACCOUNT = conf.get("sender", "account")
    PASSWORD = conf.get("sender", "password")

load_configure()
home_spider = HomeSpider(MEIDI_URL)
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)
