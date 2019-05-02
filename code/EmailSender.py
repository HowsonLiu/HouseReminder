import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class EmailSender:
    """自动发送邮件
    """
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    sender = None
    password = None
    receivers = '948470636@qq.com'    # 自己设置接受者，使用逗号隔开
    msg_text = """<html>
	<head>
		<style>
		.detail{
			margin:0 30px 0 0;
		}
		</style>
	</head>
	<body>
		<h1>{community}</h1>
		<div>
			<span class="detail" style="font-size:30px">总价格:</span>
			<span style="font-size:30px">{price}</span>
		</div>
		<div>
			<span class="detail" style="font-size:30px">建筑面积:</span>
			<span style="font-size:30px">{area}</span>
		</div>
		<div>
			<span class="detail" style="font-size:30px">单价:</span>
			<span style="font-size:30px">{perprice}</span>
		</div>
		<div>
			<span class="detail" style="font-size:30px">位置:</span>
			<span style="font-size:30px">{position}</span>
		</div>
		<div>
			<span class="detail" style="font-size:30px">户型:</span>
			<span style="font-size:30px">{pattern}</span>
		</div>
		<div>
			<a href="{url}" style="font-size:30px">链接</a>
		</div>
	</body>
</html>
    """

    def login(self):
        self.sender = input("Please enter the sender's qq email account: ")
        self.password = input("Please enter your PIN: ")
        self.server.login(self.sender, self.password)

    def send_house_info(self, houseinfo):
        send_text = self.msg_text.format(community=houseinfo.community,
                                         price=houseinfo.price,
                                         area=houseinfo.area,
                                         perprice=houseinfo.perprice,
                                         position=houseinfo.position,
                                         pattern=houseinfo.pattern,
                                         url=houseinfo.url)
        msg = MIMEText(send_text, 'html', 'utf-8')
        msg['From'] = formataddr(["Howson_Friday", self.sender])
        msg['To'] = formataddr(["You", self.receivers])
        self.server.sendmail(self.sender, [self.receivers], msg.as_string())

