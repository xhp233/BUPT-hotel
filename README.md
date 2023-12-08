# 运行服务器

对于windows系统：先运行deleteDB.bat，然后再运行runserver.bat

对于linux系统：先运行deleteDB.sh，然后再运行runserver.sh

要在同一浏览器登录不同账号，建议使用火狐的多身份标签页功能

没有的话就用不同浏览器登录

# 默认账号密码

管理员：admin admin

空调管理员：ACadmin ACadmin

前台服务员：receptionist receptionist

# 各模块功能及组员分工

## ACPanelApp - 王宇航

负责空调面板的显示和控制，向调度器发送请求。

## managerApp - 徐逅普

负责空调管理员模块，包括开关中央空调、设置中央空调状态、监控客房空调信息。

## serverApp - 王颂州

负责用户登入登出、前台开房退房及出示账单详单。

## BUPTHotelAC.scheduler.py - 高明翰

负责调度器，接收空调面板的请求，按优先级+时间片+FIFO调度。

## BUPTHotelAC.wsgi.py - 徐逅普

负责数据库与调度器的初始化，内含测试用例脚本。