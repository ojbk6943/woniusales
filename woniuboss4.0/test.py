# from interface.util.Utility import Utility
# import re
#
# def run1():
#
#     import re
#
#     # 匹配页面数据的正则
#
#     # result_recode = "显示第 1 到第 7 条记录，总共 7 条记录"
#     # result = re.match('.*，.*(\d+)', result_recode)
#     # print(result.group(1))
#
#
#
# # a = (1,2)
# # def run(a, b):
# #     print(a+b)
#
#
# # def run2():
# #     str = '{"表单数据":{"pageSize":"10","pageIndex":"2","cusInfo":"","lastStatus":"","source":"","s_time":"","e_time":"","poolType":"temp","workId":""},"请求有效载荷（payload）":{"EDITOR_CONFIG":{"text":"pageSize=10&pageIndex=2&cusInfo=&lastStatus=&source=&s_time=&e_time=&poolType=temp&workId=","mode":"application/json"}}}'
# #     print(str.split(","))
#
#
# if __name__ == '__main__':
#     sd = "2019-12-11 15:16"
#     result = re.match('20\d{2}-\d{2}-\d{2} \d{2}:\d{2}', sd)
#     print(result)
#     # run2()
#     pass
#     # run(*a)
#
#
#
#
#
#
#
#
#
# # msgs = ''
# # # print(msgs.strip())
# # print(msgs)
# # # result = re.match('^1[3456789]\d{9}$', msgs)
# # # print(result)
# # # if result:
# # #     print(result.group())
# # # else:
# # #     print("buzhi")

# 2481956455



import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 配置邮箱服务器
smtpserver = "smtp.qq.com"

# 用户/密码
user = "2481956455@qq.com"
password = "qwe19931124"

# 发送者邮箱
sender = "2481956455@qq.com"

# 接收者邮箱
receiver = "2414390944@qq.com"

# 邮件主题
subject = "Python email test"

msg = MIMEText('<html><h1>你好!</h1></html>', "html", "utf-8")
msg["Subject"] = Header(subject, "utf-8")

if __name__ == '__main__':
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver,25)
    smtp.login(user,password)
    smtp.sendmail(sender,receiver,msg.as_string())
    smtp.quit()




