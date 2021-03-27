前言：           
因为抖音带动了一次 发送名字到火星的热潮，周围人表现的十分热情，奈何他们没有墙工具

所以我突发灵感，开个淘宝店铺收费帮助注册，抱着玩玩的心，却没想到人是如此之多

因此使用 python 写下脚本 快速进行注册

## 界面式

注册完毕后，自动打开QQ邮箱为客户发送邮件    
QQ邮箱一键登录暂未写出来，所以需要QQ后台保持登录，将自动点击快捷登录.

使用方法：
```
cd 界面式
pip install selenium
pip install configparser
```
自行配置 火星船票注册系统.ini 的信息
```
start.py
```
可以支持双人

## 无界面式

注册完毕后，直接通过python的邮箱程序为客户发送邮箱（附带电子票图片）  
发送人的邮箱 需要自行在QQ邮箱里配置 POP3/SMTP 并获得密钥   

使用方法：
```
cd 无界面式
pip install configparser
pip install selenium
pip install traceback
pip install requests
```
自行配置 火星船票注册系统无界面.ini 的信息  
邮箱如何配置 自行百度  
```
start.py
```
