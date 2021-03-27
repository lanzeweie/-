#!/usr/bin/python
# -*- coding: UTF-8 -*-
#运行库
import configparser
import time
import os
import datetime
#web库
from selenium import webdriver
from selenium.webdriver.support.ui import Select

starttime = datetime.datetime.now()
rootPath = os.path.dirname(__file__)
cf = configparser.ConfigParser()
cf.read(rootPath + "\\火星船票重复注册系统.ini","utf-8")
xunhuan = int(cf.get("配置信息","循环次数"))
zong = int(cf.get("记录信息","总运行"))
name = cf.get("配置","名字")
xing = cf.get("配置","姓氏")
bianma = int(cf.get("配置","邮政编码"))
Email = cf.get("配置","邮箱")

chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chromeOptions)


for i in range(xunhuan):
    zong += 1
    zong1 = zong
    driver.get('https://mars.nasa.gov/participate/send-your-name/future')
    driver.find_element_by_xpath('//*[@id="FirstName"]').send_keys(name,"("+str(+zong1)+")")
    driver.find_element_by_xpath('//*[@id="LastName"]').send_keys(xing)
    cc = Select(driver.find_element_by_id('CountryCode'))
    cc.select_by_value("CN")                     

    driver.find_element_by_xpath('//*[@id="PostalCode"]').send_keys(bianma)      
    driver.find_element_by_xpath('//*[@id="Email"]').send_keys(Email)
    driver.find_element_by_xpath('//*[@id="submitNameForm"]/div/div[2]/button').click()
    time.sleep(1)
    i += 1 
    
endtime = datetime.datetime.now()
print ("花费",endtime - starttime,"秒")
print("运行完毕 此次运行：" +str(i) +" 次")

print("总运行次数："+str(zong1))
#记录到配置文件里
quyu = zong1 - i
print("此次注册的号码是",str(+zong),"-",str(+quyu))
cf.set("记录信息", "总运行",str(+zong1))
cf.write(open(rootPath + "\\火星船票重复注册系统.ini", "r+", encoding="utf-8"))
