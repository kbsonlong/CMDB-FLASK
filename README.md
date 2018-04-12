# 一、安装

## 1、安装沙盒环境

    pip install virtualenv

    virtualenv cmdb

    source cmdb/bin/activate

## 2、安装CMDB-FLASK

    git clone https://github.com/kbsonlong/CMDB-FLASK.git

    cd  CMDB-FLASK && pip install -r requirements.txt

## 3、修改配置

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{post}/{databasename}'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:kbsonlong@cmdb_db:3306/cmdb2'

# 二、安装集成环境

## 1、使用Docker快速搭建zabbix环境

### 安装数据库mysql

    docker run --name cmdb-db --hostname zabbix-mysql-server \
    -e MYSQL_ROOT_PASSWORD="kbsonlong" \
    -e MYSQL_USER="root" \
    -e MYSQL_PASSWORD="kbsonlong" \
    -e MYSQL_DATABASE="zabbix" \
    -p 3306:3306 \
    -d mysql:5.7 \
    --character-set-server=utf8 --collation-server=utf8_bin

### 创建zabbix-server

    docker run  --name cmd-zabbix-server-mysql --hostname zabbix-server-mysql \
    --link cmdb-db:mysql \
    -e DB_SERVER_HOST="mysql" \
    -e MYSQL_USER="root" \
    -e MYSQL_DATABASE="zabbix" \
    -e MYSQL_PASSWORD="kbsonlong" \
    -v /etc/localtime:/etc/localtime:ro \
    -v /data/docker/zabbix/alertscripts:/usr/lib/zabbix/alertscripts \
    -v /data/docker/zabbix/externalscripts:/usr/lib/zabbix/externalscripts \
    -p 10051:10051 \
    -d \
    zabbix/zabbix-server-mysql

### 安装web-nginx

    docker run --name cmd-zabbix-web-nginx-mysql --hostname zabbix-web-nginx-mysql \
    --link cmdb-db:mysql \
    --link cmd-zabbix-server-mysql:zabbix-server \
    -e DB_SERVER_HOST="mysql" \
    -e MYSQL_USER="root" \
    -e MYSQL_PASSWORD="kbsonlong" \
    -e MYSQL_DATABASE="zabbix" \
    -e ZBX_SERVER_HOST="zabbix-server" \
    -e PHP_TZ="Asia/Shanghai" \
    -p 8000:80 \
    -p 8443:443 \
    -d \
    zabbix/zabbix-web-nginx-mysql

### 安装zabbix-agent

    docker run --name cmdb-zabbix-agent --link cmd-zabbix-server-mysql:zabbix-server -d zabbix/zabbix-agent:latest
