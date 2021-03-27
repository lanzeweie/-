# -*- coding: utf-8 -*-  运行库存 1:os 2:配置ini 3:浏览器程序 4:浏览器元素 5:点击
import os
import configparser
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


#打开谷歌浏览器
driver = webdriver.Chrome(executable_path="chromedriver.exe")
#浏览器窗口全屏显示
driver.maximize_window()
#打开网页
driver.get('https://mars.nasa.gov/participate/send-your-name/future')

# 获得当前目录 读取配置信息
rootPath = os.path.dirname(__file__)
cf = configparser.ConfigParser()
cf.read(rootPath + "\\火星船票注册系统.ini","utf-8")

# 初始化配置信息
FIRST = cf.get("火星船票信息配置","名字")
LAST = cf.get("火星船票信息配置","姓氏")
POSTAL = cf.get("火星船票信息配置","邮政编码")
EMAIL = cf.get("火星船票信息配置","邮箱")
TONGZHI = cf.get("火星船票信息配置","接收后续通知")
SHUANGREN = cf.get("火星船票信息配置","双人票")
#是否进行双人票模式
if SHUANGREN =="是":
    FIRST2 = cf.get("火星船票信息配置","名字t")
    LAST2 = cf.get("火星船票信息配置","姓氏t")
    POSTAL2 = cf.get("火星船票信息配置","邮政编码t")
    EMAIL2 = cf.get("火星船票信息配置","邮箱t")
    TONGZHI2 = cf.get("火星船票信息配置","接收后续通知t")
    print('当前模式为双人模式')


## 自动化操作开始！
driver.find_element_by_xpath('//*[@id="FirstName"]').send_keys(FIRST)
driver.find_element_by_xpath('//*[@id="LastName"]').send_keys(LAST)
#选择框定位
cc = Select(driver.find_element_by_id('CountryCode'))
cc.select_by_value("CN")                     

driver.find_element_by_xpath('//*[@id="PostalCode"]').send_keys(POSTAL)      
driver.find_element_by_xpath('//*[@id="Email"]').send_keys(EMAIL)    
#是否需要接受NASA后续通知
if TONGZHI =="是":
    driver.find_element_by_xpath('//*[@id="newsletter"]').click()  

driver.find_element_by_xpath('//*[@id="submitNameForm"]/div/div[2]/button').click()  
#结束!

#获得电子票链接
time.sleep(3)
URL = driver.current_url
print(URL)

#是否进行双人票模式
if SHUANGREN =="是":
    driver.execute_script("window.open('https://mars.nasa.gov/participate/send-your-name/future');")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    ## 自动化操作开始！
    driver.find_element_by_xpath('//*[@id="FirstName"]').send_keys(FIRST2)
    driver.find_element_by_xpath('//*[@id="LastName"]').send_keys(LAST2)
    #选择框定位
    cc = Select(driver.find_element_by_id('CountryCode'))
    cc.select_by_value("CN")                     

    driver.find_element_by_xpath('//*[@id="PostalCode"]').send_keys(POSTAL2)      
    driver.find_element_by_xpath('//*[@id="Email"]').send_keys(EMAIL2)    
    #是否需要接受NASA后续通知
    if TONGZHI2 =="是":
        driver.find_element_by_xpath('//*[@id="newsletter"]').click()  

    driver.find_element_by_xpath('//*[@id="submitNameForm"]/div/div[2]/button').click()  
    #结束!

    #获得电子票链接
    time.sleep(2)
    URL2 = driver.current_url
    print(URL2)



#转到新页面+切换元素控制
driver.execute_script("window.open('https://mail.qq.com/');")
time.sleep(1)
driver.switch_to.window(driver.window_handles[-1])

#登录QQ邮箱
print("开始模块：",driver.title)
ActionChains(driver).move_by_offset(1325,390).click().perform() # 鼠标左键点击
print("正在进入QQ邮箱")
time.sleep(5)
#QQ邮箱自动化
driver.find_element_by_xpath('//*[@id="composebtn"]').click()  #定位至写信
# 切换到mainFrame
driver.switch_to.frame('mainFrame')
time.sleep(1)
# 定位收件人，并输入
driver.find_element_by_xpath("//*[@id='toAreaCtrl']/div[2]/input").send_keys(EMAIL)
# 定位主题，并输入
driver.find_element_by_xpath('//*[@id="subject"]').send_keys("您所预定的2026火星船票")
# 定位邮件正文，先进入到iframe
driver.switch_to.frame(driver.find_element_by_xpath('//*[@class="qmEditorIfrmEditArea"]'))
# 必须先点击正文，再send_keys
driver.find_element_by_xpath('/html/body').click()

# 写入文本！ 分 单双人文本
if SHUANGREN =="是":
    driver.find_element_by_xpath('/html/body').send_keys(
                                                          "船员："+LAST,"_"+FIRST,"\n船员："+LAST2,"_"+FIRST2,"\n欢迎登船","\n您的名字已经被刻录到了火星飞船的数据库里",
                                                          "\n将在2026年随着宇宙飞船发射至火星！","\n","\n这是您的 2026年 火星船票 请查收","\n祝您好运！","\n","\n电子票已经为您存放入附件(邮件中下滑即可出现)",
                                                          "\n如有需要 可在","\n"+URL,"-"+LAST,"_"+FIRST,"\n"+URL2,"-"+LAST2,"_"+FIRST2,"\n查询到您的信息","\n感谢 您的预定","\n","\n白熊的私人杂货铺","\n为您献上祝福！") 
else:
    driver.find_element_by_xpath('/html/body').send_keys(
                                                          "船员："+LAST,"_"+FIRST,"\n欢迎登船","\n您的名字已经被刻录到了火星飞船的数据库里",
                                                          "\n将在2026年随着宇宙飞船发射至火星！","\n","\n这是您的 2026年 火星船票 请查收","\n祝您好运！","\n","\n电子票已经为您存放入附件(邮件中下滑即可出现)",
                                                          "\n如有需要 可在","\n"+URL,"\n查询到您的信息","\n感谢 您的预定","\n","\n白熊的私人杂货铺","\n为您献上祝福！") 

# 返回到mainframe
driver.switch_to.parent_frame()
print("已完毕")



