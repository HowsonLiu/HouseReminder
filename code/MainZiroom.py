from WebsiteZiroom import *

ziroom_spider = ZiroomSpider(TARGET_URL)
num = ziroom_spider.get_page_num()
print(num)
houses = ziroom_spider.get_house_list(1)
print(houses)