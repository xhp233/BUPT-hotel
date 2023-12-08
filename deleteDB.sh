#!/bin/bash

# 定义一个函数来删除__pycache__和migrations目录
function delete_dir {
    rm -rf "$1/__pycache__"
    find "$1/migrations" -mindepth 1 ! -name '__init__.py' -delete
}

# 对每个应用执行删除操作
for app in serverApp managerApp ACPanelApp BUPTHotelAC
do
    delete_dir "$app"
done

# 删除数据库文件
rm -f BUPTHotelAC.db