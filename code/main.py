from EmailSender import EmailSender
from WebsiteAnjuke import *
import schedule
import time

REFERSH_INTERVAL = 30

def check_and_send():
    global home_spider, old_url, sender
    lastest_url = home_spider.get_first_url()
    if lastest_url == old_url:
        return False
    detail_spider = DetailSpider(lastest_url)
    houseinfo = detail_spider.get_houseinfo()
    sender.send_house_info(houseinfo)
    old_url = lastest_url
    print(lastest_url)
    return True

old_url = None
home_spider = HomeSpider(SHUNDE_URL)
sender = EmailSender()
sender.login()
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)