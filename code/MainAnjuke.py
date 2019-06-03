# -*- coding:utf8 -*-
from EmailSender import *
from WebsiteAnjuke import *
import schedule
import time

REFERSH_INTERVAL = 60
HOME_SPIDER = None
OLD_URL = None


def check_and_send():
    global HOME_SPIDER, OLD_URL
    lastest_url = HOME_SPIDER.get_first_url()
    print(time.strftime("%Y-%m-%d %H:%M:%S is running", time.localtime()))
    if OLD_URL is not None and lastest_url is not None and lastest_url[:-20] == OLD_URL[:-20]:      # 除去url中的时间干扰
        return False
    detail_spider = DetailSpider(lastest_url)
    houseinfo = detail_spider.get_houseinfo()
    if houseinfo is None:
        print('Get Detail Error')
        return False
    sender = EmailSender()
    try:
        sender.default_login()
        sender.anjuke_send_house_info(houseinfo)
        OLD_URL = lastest_url
        print(lastest_url)
    except Exception as e:
        print('SMTP connected error: ' + repr(e))
        return False
    return True

load_email_configure()
HOME_SPIDER = HomeSpider(MEIDI_URL)
check_and_send()
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)
