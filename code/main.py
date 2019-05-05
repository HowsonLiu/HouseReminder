# -*- coding:utf8 -*-
from EmailSender import EmailSender
from WebsiteAnjuke import *
import schedule
import configparser
import time

REFERSH_INTERVAL = 30
CONFIG_FILE_PATH = "./setup.cfg"

def check_and_send():
    global home_spider, old_url, sender
    lastest_url = home_spider.get_first_url()
    print(lastest_url)
    if old_url is not None and lastest_url is not None and lastest_url[:-20] == old_url[:-20]:      # 除去url中的时间干扰
        return False
    detail_spider = DetailSpider(lastest_url)
    houseinfo = detail_spider.get_houseinfo()
    sender.send_house_info(houseinfo)
    old_url = lastest_url
    return True

def load_configure():
    conf = configparser.ConfigParser()
    conf.read(CONFIG_FILE_PATH, encoding='utf-8')
    account = conf.get("sender", "account")
    password = conf.get("sender", "password")
    return account, password

old_url = None
account, password = load_configure()
home_spider = HomeSpider(MEIDI_URL)
sender = EmailSender()
sender.login(account, password)
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)
