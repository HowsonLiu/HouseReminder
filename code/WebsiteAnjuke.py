import requests

# 顺德 最新
SHUNDE_URL = 'https://foshan.anjuke.com/sale/shundequ/o5/'

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



