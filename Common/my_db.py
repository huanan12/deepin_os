# 封装数据库  ---废弃
"""
MyDb            mysql数据库读取
get_one_db      获取单条sql数据
get_all_db      获取所有sql数据结果
get_count_db    获取数据结果条数
update_db       修改数据库数据
close           关闭数据数据链接
"""
import pymysql
from Common.do_config import conf

class myERROR(Exception):
    pass

class MyDb:
    # 1.连接数据库
    # print(conf.get("mysql_deepin", "host"))
    def __init__(self):
        self.conn = pymysql.connect(
            host=conf.get(conf.get("mydb", "dbName"), "host"),
            port=int(conf.get(conf.get("mydb", "dbName"), "port")),
            user=conf.get(conf.get("mydb", "dbName"), "user"),
            password=conf.get(conf.get("mydb", "dbName"), "password"),
            database=conf.get(conf.get("mydb", "dbName"), "database"),
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor  # 数组转为字典
        )

        # 2.创建游标
        self.cur = self.conn.cursor()

    # 获取单条数据结果
    def get_one_db(self,sql):
        self.conn.commit()
        # 3.执行sql语句
        self.cur.execute(sql)
        # 4.执行sql语句,获取数据结果
        return self.cur.fetchone()

    # 获取所有数据结果
    def get_all_db(self,sql):
        self.conn.commit()
        # 3.执行sql语句
        self.cur.execute(sql)
        # 4.执行sql语句,获取数据结果
        return self.cur.fetchall()

    # 获取数据结果条数
    def get_count_db(self,sql):
        self.conn.commit()
        # 3.执行sql语句
        count = self.cur.execute(sql)
        # 4.执行sql语句,获取数据结果
        return count

    # 修改数据库
    def update_db(self,sql):
        # 3.执行sql语句
        self.cur.execute(sql)
        # 4.保存数据库
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()



if __name__ == '__main__':
    mydb = MyDb()
    # sql = 'SELECT * FROM image WHERE  uid = 20458 limit 3'
    # sql = 'insert into oks(name,age,tel) values("小明",19,"13567823931")'
    # result = mydb.get_all_db(sql)
    sql = 'select * from oks'
    # sql = 'use tear'
    for sql_value in result:
        print(sql_value)
    # print(result)

    mydb.close()