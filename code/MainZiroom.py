from WebsiteZiroom import *
from EmailSender import *
import schedule
import time

REFERSH_INTERVAL = 60
HOME_SPIDER = None
OLD_ALL_HOUSE_LIST = []


def check_and_send_ziroom():
    global HOME_SPIDER, OLD_ALL_HOUSE_LIST
    print(time.strftime("%Y-%m-%d %H:%M:%S is running", time.localtime()))
    all_house_list, res = HOME_SPIDER.get_all_house_list()
    if res is False:
        print("Get all houses error")
        return False
    if len(OLD_ALL_HOUSE_LIST) < 1:
        OLD_ALL_HOUSE_LIST = all_house_list
        return True
    new_houses = set(all_house_list) - set(OLD_ALL_HOUSE_LIST)
    for new_house in new_houses:
        try:
            sender = EmailSender()
            sender.default_login()
            sender.ziroom_send_house_link(new_house)
            print(new_house)
        except Exception as e:
            print('SMTP connected error: ' + repr(e))
            return False
    return True


load_email_configure()
HOME_SPIDER = ZiroomSpider(TARGET_URL)
check_and_send_ziroom()
schedule.every(REFERSH_INTERVAL).seconds.do(check_and_send_ziroom)
while True:
    schedule.run_pending()
    time.sleep(1)

