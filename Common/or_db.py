"""
数据库链接   未验证

"""

import cx_Oracle
from Common.do_config import conf
user = conf.get("mysql", "user")
password = conf.get("mysql", "password")
host = conf.get("mysql", "host") + ":" + conf.get("mysql", "port") + "/" + conf.get("mysql", "database")
print(user,password,host)
con = cx_Oracle.connect(user,password,host)

cursor = con.cursor()       #创建游标
sql = 'SELECT * FROM image WHERE  uid = 20458 limit 3'
cursor.execute(sql)  #执行sql语句
data = cursor.fetchone()        #获取一条数据
print(data)     #打印数据
cursor.close()  #关闭游标
con.close()     #关闭数据库连接