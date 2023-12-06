# 运行服务器

先运行deleteDB.bat，然后再运行runserver.bat

# 默认账号密码

管理员：admin admin

空调管理员：ACadmin ACadmin

前台服务员：receptionist receptionist

# 为某一功能实现前后端

1. 在...App文件夹中的views.py里定义后端函数
2. 在BUPTHotelAC文件夹中的urls.py中绑定后端函数响应的网址

# ...App

## \_\_init\_\_.py

空的，不用动

## admin.py

一般不需要写东西，仅当注册管理员类时要写

## apps.py

一般不需要写东西，注册app用，已写好

## models.py

定义用到的数据库结构

## tests.py

一般不需要写东西，写测试用例用

## views.py

写对于某一网址的响应函数

## static（文件夹）

存放css、js文件，默认不存在，需自己创建

## templates（文件夹）

存放html文件，默认不存在，需自己创建

## migrations（文件夹）

平常不要动

# BUPTHotelAC

## asgi.py

没用

## settings.py

全局设置

## urls.py

注册网址与后端的响应函数的绑定关系

## wsgi.py

每次启动服务器时自动运行，内含一些初始化操作