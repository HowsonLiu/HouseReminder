# -*- coding:utf8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class EmailSender:
    """自动发送邮件
    """
    server = None
    sender = None
    password = None     # vjqmcgyoulifciej
    receivers = ['948470636@qq.com', '1819976230@qq.com', '2848727944@qq.com']
    msg_text = r"""<html><head><style>.detail{margin:0 30px 0 0;}</style>
</head><body><h1>%s</h1><div><span class="detail" style="font-size:30px">总价格:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">建筑面积:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">单价:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">位置:</span>
<span style="font-size:30px">%s</span></div><div><span class="detail" style="font-size:30px">户型:</span>
<span style="font-size:30px">%s</span></div><div><a href="%s" style="font-size:30px">链接</a></div></body>
</html>"""

    def login(self, account, password):
        self.server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        self.sender = account
        self.password = password
        self.server.login(self.sender, self.password)
        print("login success")

    def send_house_info(self, houseinfo):
        send_text = self.msg_text % (houseinfo.community,
                                     houseinfo.price,
                                     houseinfo.area,
                                     houseinfo.perprice,
                                     houseinfo.position,
                                     houseinfo.pattern,
                                     houseinfo.url)
        msg = MIMEText(send_text, 'html', 'utf-8')
        msg['From'] = formataddr(["Howson_Friday", self.sender])
        msg['To'] = ", ".join(self.receivers)
        msg['Subject'] = houseinfo.community + " " + houseinfo.area + " " + houseinfo.price
        self.server.sendmail(self.sender, self.receivers, msg.as_string())

