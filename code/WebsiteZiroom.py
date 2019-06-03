# -*- coding:utf8 -*-
import requests
from bs4 import BeautifulSoup

# 百度科技园附近
TARGET_URL = 'http://www.ziroom.com/z/nl/z3-s16%E5%8F%B7%E7%BA%BF-t%E8%A5%BF%E5%8C%97%E6%97%BA-o1.html'

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36'
}


class ZiroomSpider:
    """自如爬虫
    """

    url = None

    def __init__(self, url):
        self.url = url

    def get_page_num(self):
        """获取页数"""
        if self.url is None:
            return 0
        try:
            html = requests.get(self.url, headers=HEADER)
            if html.status_code != 200:
                print('Get page number response ' + str(html.status_code))
                return 0
        except Exception as e:
            print('Get page number error:' + repr(e))
            return 0
        soup = BeautifulSoup(html.text, 'lxml')
        number_text = soup.select('body > div.t_myarea.t_mainbox.clearfix.mt15.t_zindex0 > div > '
                                  'div.t_shuaichoose_order > div > span')[0].get_text()
        number = int(number_text[2:])   # 1/10去除1/
        return number

    def get_house_list(self, index):
        house_list = []
        if self.url is None or index < 1:
            return house_list, False
        url = self.url + '?p=' + str(index)
        try:
            html = requests.get(url, headers=HEADER)
            if html.status_code != 200:
                print('Get' + str(index) + ' page response ' + str(html.status_code))
                return house_list, False
        except Exception as e:
            print('Get' + str(index) + ' page error:' + repr(e))
            return house_list, False
        soup = BeautifulSoup(html.text, 'lxml')
        house_list_soup = soup.select('#houseList > li')  # 找出houseList下所有的li
        for house in house_list_soup:
            href = house.select('div.priceDetail > p.more > a')[0]['href']  # 要加[0]，否则是NavigableString对象
            house_list.append(href[2:])  # 去除前面的//
        return house_list, True

    def get_all_house_list(self):
        page_num = self.get_page_num()
        all_house_list = []
        for index in range(1, page_num+1):
            house_list, res = self.get_house_list(index)
            if res is False:
                return [], False
            all_house_list.extend(house_list)
        return all_house_list, True

