#!/bin/bash

# 检查MySQL是否已安装
if ! command -v mysql &> /dev/null; then
    # 如果未安装，使用apt安装MySQL
    echo "MySQL未安装，正在安装..."
    sudo apt update
    sudo apt install mysql-server

    # 启动MySQL服务
    sudo systemctl start mysql

    # 设置MySQL root密码（这里使用示例密码，应替换为实际密码）
#    sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH 'mysql_native_password' BY 'your_root_password';"

    # 允许远程访问，如果需要
    # sudo mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'your_root_password' WITH GRANT OPTION;"
    # sudo mysql -e "FLUSH PRIVILEGES"

    echo "MySQL已安装并初始化配置完成."
fi

# 连接到MySQL数据库
echo "连接到MySQL数据库..."
mysql -u user -h 192.168.8.175 -p
