# 随机生成手机号码
"""
NewPhone        手机号生成器
new_tols        随机生成手机号
check_phone_db   校验数据库是否存在手机号已经注册   （业务逻辑忽略）
"""
import random



from Common.my_db import MyDb
from Common.my_requests import chen_request
from Common.my_logger import logger
from Common.do_config import conf

class NewPhone:
    def new_tols(self):
        # 随机生成一个新的手机号码
        # yidong = [134,135,136,137,138,139,147,150,151,152,157,158,159,172,178,182,183,184,187,188,195,197,198]
        # liantong = [130,131,132,145,155,156,166,175,176,185,186,196]
        # dianxin = [133,149,153 ,180 ,181 ,189,173,177,190,191,193,199]
        # guandian = [192]
        # phone = yidong + liantong + dianxin + guandian

        phone = [177,150,132]

        num = random.randint(0,len(phone)-1)
        new_tol = str(phone[num])
        for i in range(8):
            new_tol = new_tol + str(random.randint(0,9))

        return new_tol

    def check_phone_db(self):
        # 校验新生成的手机号是否在数据库存在，不存在就返回新号码注册
        mydb = MyDb()     #一定不能忘记，不然第二次调用报错，数据库已经断开连接
        while True:

            news = self.new_tols()
            count = mydb.get_all_db('select * from member where mobile_phone = {}'.format(str(news)))
            if count == ():
                mydb.close()  #数据库用完后关闭连接
                return news

    def register_tol(self):
        # 注册
        # phone = conf.get("loging","mobile_phone")
        phone = conf.get("loging",conf.get("loging","is_admin_user"))

        mydb = MyDb()
        sql = "select * from member where mobile_phone={}".format(phone)
        count = mydb.get_count_db(sql)
        if count == 0:
            url = "member/register"
            # pwd = conf.get("loging","pwd")
            pwd = conf.get("loging", conf.get("loging", "is_pwd_admin_user"))
            type = int(conf.get("loging","type"))
            data = {"mobile_phone": phone, "pwd": pwd,"type":type}
            logger.info("注册的电话号码为：{}".format(phone))
            logger.info("注册的密码为：{}".format(pwd))
            res = chen_request("post", url, data)
            # print(res.json())
            logger.info("注册响应内容为：{}".format(res.json()))

        mydb.close()

new_tol = NewPhone()

if __name__ == '__main__':
    # print(new_tol.new_tols())
    # print(new_tol.new_tols())
    new_tol.register_tol()