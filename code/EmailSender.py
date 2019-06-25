# -*- coding:utf8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser

ACCOUNT = None
PASSWORD = None
CONFIG_FILE_PATH = "./code/setup.cfg"


def load_email_configure():
    """加载邮件发送方账号与密码(全局)"""
    global ACCOUNT, PASSWORD
    conf = configparser.ConfigParser()
    conf.read(CONFIG_FILE_PATH, encoding='utf-8')
    ACCOUNT = conf.get("sender", "account")
    PASSWORD = conf.get("sender", "password")


class EmailSender:
    """自动发送邮件
    """
    server = None
    sender = None
    password = None

    anjuke_receivers = ['948470636@qq.com', '1819976230@qq.com', '2848727944@qq.com']
    anjuke_msg_text = r"""<html><head><style>.detail{margin:0 30px 0 0;}</style>
</head><body><h1>%s</h1><div><span class="detail" style="font-size:30px">总价格:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">建筑面积:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">单价:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">位置:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">户型:</span>
<span style="font-size:30px">%s</span></div><div><a href="%s" style="font-size:30px">链接</a></div></body>
</html>"""

    ziroom_receivers = ['948470636@qq.com']
    ziroom_msg_text = r"""<html><head><h1><a href="%s">%s</a></h1></head></html>"""

    def default_login(self):
        global ACCOUNT, PASSWORD
        self.server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        self.sender = ACCOUNT
        self.password = PASSWORD
        self.server.login(self.sender, self.password)
        print("login success")

    def login(self, account, password):
        self.server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        self.sender = account
        self.password = password
        self.server.login(self.sender, self.password)
        print("login success")

    def anjuke_send_house_info(self, houseinfo):
        send_text = self.anjuke_msg_text % (houseinfo.community,
                                            houseinfo.price,
                                            houseinfo.area,
                                            houseinfo.perprice,
                                            houseinfo.position,
                                            houseinfo.pattern,
                                            houseinfo.url)
        msg = MIMEText(send_text, 'html', 'utf-8')
        msg['From'] = formataddr(["Howson_Friday", self.sender])
        msg['To'] = ", ".join(self.anjuke_receivers)
        msg['Subject'] = houseinfo.community + " " + houseinfo.area + " " + houseinfo.price
        self.server.sendmail(self.sender, self.anjuke_receivers, msg.as_string())

    def ziroom_send_house_link(self, link):
        send_text = self.ziroom_msg_text % (link, link)
        msg = MIMEText(send_text, 'html', 'utf-8')
        msg['From'] = formataddr(["Howson_Friday", self.sender])
        msg['To'] = ", ".join(self.anjuke_receivers)
        msg['Subject'] = "Ziroom new house"
        self.server.sendmail(self.sender, self.ziroom_receivers, msg.as_string())
