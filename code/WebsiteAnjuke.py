# -*- coding:utf8 -*-
import requests
from bs4 import BeautifulSoup

# 顺德 最新
SHUNDE_URL = 'https://foshan.anjuke.com/sale/shundequ/o5/'
# 美的海岸花园 最新
MEIDI_URL = 'https://foshan.anjuke.com/sale/o5/?kw=%E7%BE%8E%E7%9A%84%E6%B5%B7%E5%B2%B8%E8%8A%B1%E5%9B%AD&k_' \
            'comm_id=261039&kw_type=3'

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36'
}


class HouseInfo:
    """安居客网站房屋信息结构
    """
    url = None          # 链接
    price = None        # 总价格
    perprice = None     # 元/m2
    area = None         # 建筑面积
    pattern = None      # 户型
    community = None    # 小区
    position = None     # 位置


class HomeSpider:
    """安居客首页爬虫
    """
    url = None

    def __init__(self, url):
        self.url = url

    def get_first_url(self):
        """获取下面列表第一个房子的url"""
        if self.url is None:
            print('Warning: url is None')
            return None
        try:
            html = requests.get(self.url, headers=HEADER)
            if html.status_code != 200:
                print('Warning: Status code is ' + str(html.status_code))
                return None
        except Exception as e:
            print('Error: Can not get first url')
            print(repr(e))
            return None
        soup = BeautifulSoup(html.text, 'lxml')
        house_list = soup.select('#houselist-mod-new > li:nth-child(1) > div.house-details > div.house-title > a')
        if len(house_list) == 0:
            print('Warning: bs4 error')
            return None
        href = house_list[0].get("href")
        return href


class DetailSpider:
    """安居客详情页爬虫
    """
    url = None

    def __init__(self, url):
        self.url = url

    def get_houseinfo(self):
        if self.url is None:
            print('Warning: url is None')
            return None
        try:
            html = requests.get(self.url, headers=HEADER)
            if html.status_code != 200:
                print('Warning: Status code is ' + str(html.status_code))
                return None
        except Exception as e:
            print('Error: Can not get detail page')
            print(repr(e))
            return
        soup = BeautifulSoup(html.text, 'lxml')
        info = HouseInfo()
        # url
        info.url = self.url
        # price
        try:
            info.price = soup.select('#content > div.wrapper > div.wrapper-lf > div.clearfix > '
                                     'div.basic-info.clearfix > span.light.info-tag > em')[0].string
            info.price = info.price + "万"
        except Exception:
            info.price = "?万"
        # perprice
        try:
            info.perprice = soup.select('#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > '
                                        'div.houseInfo-wrap > ul > li:nth-child(3) > div.houseInfo-content')[0].string
        except:
            info.perprice = "?元/m2"
        # area
        try:
            info.area = soup.select('#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > '
                                    'div.houseInfo-wrap > ul > li:nth-child(5) > div.houseInfo-content')[0].string
        except:
            info.area = "?平方米"
        # pattern
        try:
            info.pattern = soup.select('#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > '
                                       'div.houseInfo-wrap > ul > li:nth-child(2) > div.houseInfo-content')[0].string
            info.pattern = info.pattern.replace('\n', '')
            info.pattern = info.pattern.replace('\t', '')
        except:
            info.pattern = "?室?厅?卫"
        # community
        try:
            info.community = soup.select('#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > div > '
                                         'div.houseInfo-wrap > ul > li:nth-child(1) > div.houseInfo-content > '
                                         'a')[0].string
        except:
            info.community = "?"
        # position
        try:
            info.position = soup.select('#content > div.wrapper > div.wrapper-lf > div.houseInfoBox > '
                                                        'div > div.houseInfo-wrap > ul > li:nth-child(4) > '
                                                        'div.houseInfo-content > p')[0].get_text()
            info.position = info.position.replace(' ', '')
            info.position = info.position.replace('\n', '')
            info.position = info.position.replace('－', ' ')
        except:
            info.position = "?"
        return info

