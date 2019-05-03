from EmailSender import EmailSender
from WebsiteAnjuke import *
import schedule
import time

REFERSH_INTERVAL = 30

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

old_url = None
home_spider = HomeSpider(MEIDI_URL)
sender = EmailSender()
sender.login()
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)
