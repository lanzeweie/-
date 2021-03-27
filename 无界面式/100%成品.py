#运行库
import configparser
import time
import shutil
import requests
import os
import traceback
#web库
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
#邮件库
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

print('成功加载：火星船票注册系统 作者：lanzeweie@foxmail.com')
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
# 创建下载目录
if os.path.exists('imgs'):
    print("目录已经有imgs")
else:
    os.makedirs('imgs')

#开始！
#基础配置信息

# 修改下载目录
lujin = os.path.dirname(__file__)
img = lujin + "\imgs"
time.sleep(1)
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--headless') #静默运行
prefs = {"download.default_directory":img}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
#浏览器窗口全屏显示
driver.maximize_window()
driver.get('https://mars.nasa.gov/participate/send-your-name/future')

#读取配置ini
# 获得当前目录 读取配置信息
rootPath = os.path.dirname(__file__)
cf = configparser.ConfigParser()
cf.read(rootPath + "\\火星船票注册系统无界面.ini","utf-8")

# 初始化配置信息
FIRST = cf.get("火星船票信息配置","名字")
LAST = cf.get("火星船票信息配置","姓氏")
POSTAL = cf.get("火星船票信息配置","邮政编码")
EMAIL = cf.get("火星船票信息配置","邮箱")
TONGZHI = cf.get("火星船票信息配置","接收后续通知")
send_email1 = cf.get("火星船票信息配置","发件人邮箱")
miyao = cf.get("火星船票信息配置","密钥")

#清空 imgs 文件夹
def  del_file(path):
      if not os.listdir(path):
            print('目录为空！')
      else:
            for i in os.listdir(path):
                  print('开始清理')
                  path_file = os.path.join(path,i)  #取文件绝对路径
                  print(path_file)
                  if os.path.isfile(path_file):
                        os.remove(path_file)
                  else:
                        del_file(path_file)
                        shutil.rmtree(path_file)
if __name__ == '__main__':
      path=img
      del_file(path)

print("已经完成基本配置")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("开始注册网页信息")

## 自动化操作开始！
driver.find_element_by_xpath('//*[@id="FirstName"]').send_keys(FIRST)
driver.find_element_by_xpath('//*[@id="LastName"]').send_keys(LAST)
#选择框定位
cc = Select(driver.find_element_by_id('CountryCode'))
cc.select_by_value("CN")                     

driver.find_element_by_xpath('//*[@id="PostalCode"]').send_keys(POSTAL)      
driver.find_element_by_xpath('//*[@id="Email"]').send_keys(EMAIL)
time.sleep(0.5)    
#是否需要接受NASA后续通知
if TONGZHI =="是":
    driver.find_element_by_xpath('//*[@id="newsletter"]').click()  
    print('我已经勾选消息啦')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="submitNameForm"]/div/div[2]/button').click()
xiazai = "ok"  
#下载附件!
time.sleep(2)
if xiazai == "ok":
    time.sleep(3)
    driver.find_element_by_id('downloadTicket').click()
#完成结束！

#获得信息
#当前网站链接
time.sleep(3)
URL = driver.current_url
print(URL)
#附件图片的位置
time.sleep(2)
if not os.listdir(img):
    print('无法找到图片文件,请重试')
    exit()
else:
    for i1 in os.listdir(img):
        path_file1 = os.path.join(img,i1)  #取文件绝对路径
        print(path_file1)
        print('成功捕捉到图片文件')
        webed = "jiesu"
        driver.quit()

print("已经完成基本信息！")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")
print("-----------------------------------------------------")

#邮箱模块启动
if webed == "jiesu":
      print("准备启动邮箱模块")
      time.sleep(2)
      def send_email(receivers, topic, content, sender=send_email1, password=miyao):
          # 自己填好相关信息
          for receiver in receivers:
              try:
                  msg = MIMEMultipart()
                  msg['From'] = Header(sender, 'utf-8')  # 编辑邮件头
                  msg['To'] = Header(receiver, 'utf-8')
                  msg['Subject'] = Header(topic, 'utf-8')
                  msg.attach(MIMEText(content, 'plain', 'utf-8'))  # 把正文附在邮件上

                  with open(path_file1, 'rb') as f:
                      mime = MIMEBase('image', 'png', filename='Hello.png')  # 创建表示附件的MIMEBase对象，重新命名为test.png
                      mime.add_header('Content-Disposition', 'attachment', filename='电子票.png')
                      mime.set_payload(f.read())  # 读取附件内容
                      encoders.encode_base64(mime)  # 对附件Base64编码
                      msg.attach(mime)  # 把附件附在邮件上
                      server = SMTP('smtp.qq.com', 25)
                      server.login(sender, password)
                      server.sendmail(sender, receiver, msg.as_string())
                      print('发送成功！')
              except Exception as error:
                  print(error)
                  continue

if __name__ == '__main__':
    receiver = [EMAIL]
    topic = '您所预定的2026火星船票'
    content =  ("船员："+LAST+"_"+FIRST+"\n欢迎登船"+"\n您的名字已经被刻录到了火星飞船的数据库里"+
                "\n将在2026年随着宇宙飞船发射至火星！"+"\n"+"\n这是您的 2026年 火星船票 请查收"+"\n祝您好运！"+"\n"+"\n电子票已经为您存放入附件(邮件中下滑即可出现)"+
                "\n如有需要 可在"+"\n"+URL+"\n查询到您的信息"+"\n感谢 您的预定"+"\n"+"\n白熊的私人杂货铺"+"\n为您献上祝福！"
                )
    send_email(receiver, topic, content)

time.sleep(2)
driver.quit()

    