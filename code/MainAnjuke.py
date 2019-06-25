# -*- coding:utf8 -*-
from EmailSender import *
from WebsiteAnjuke import *
import schedule
import time

PRINT_INTERVAL = 5
REFERSH_INTERVAL = 60
HOME_SPIDER = None
OLD_URL = None


def check_and_send():
    global HOME_SPIDER, OLD_URL, PRINT_INTERVAL
    PRINT_INTERVAL -= 1
    if PRINT_INTERVAL == 0:
        print(time.strftime("Note: %Y-%m-%d %H:%M:%S is running", time.localtime()))
        PRINT_INTERVAL = 5
    lastest_url = HOME_SPIDER.get_first_url()
    if lastest_url is None:
        return False
    # 安居客更新了一个uniqid字段，也需要筛除去
    if OLD_URL is not None and lastest_url is not None and lastest_url[:50] == OLD_URL[:50]:
        return False
    detail_spider = DetailSpider(lastest_url)
    houseinfo = detail_spider.get_houseinfo()
    if houseinfo is None:
        return False
    sender = EmailSender()
    try:
        sender.default_login()
        sender.anjuke_send_house_info(houseinfo)
        OLD_URL = lastest_url
        print('Note: Newest url is: ' + lastest_url[:47])
    except Exception as e:
        print('Error: SMTP connected error')
        print(repr(e))
        return False
    return True

load_email_configure()
HOME_SPIDER = HomeSpider(MEIDI_URL)
check_and_send()
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)
