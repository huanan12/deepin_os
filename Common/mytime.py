# 时间

import time ,datetime

class GetTime:
    def get_time(self,time_num = time.time()):
        """
        时间戳转为时间
        :param time_num: 时间戳 1694999432.7735808
        :return: 时间 2023-09-18 09:13:38
        """
        timestamp = time_num
        timeArray = time.localtime(timestamp)
        formatTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return formatTime

    def get_times(self,time_num = time.time()):
        """
        时间戳转为时间
        :param time_num: 时间戳 1694999432.7735808
        :return: 时间 2023-09-18 09:13:38
        """
        timestamp = int(time_num)

        # 将时间戳转换为结构化时间
        t = time.gmtime(timestamp)

        # 将 UTC 结构化时间转换为本地时间结构化时间
        local_time = time.localtime(time.mktime((t)) + 8 * 60 * 60)

        # 格式化时间
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        return time_str

    def get_tiem_int(self,time_num):
        """
        时间格式转为时间戳
        :param time_num: 时间格式 2023-09-18 09:13:38
        :return: 时间戳 1694999432
        """
        times = time.strptime(time_num, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(times))
        return timestamp

    def get_year(self,time_num = time.time()):
        """
        时间戳获取年份
        :param time_num: 时间戳
        :return: 年
        """
        timestamp = time_num
        ftimeArray = time.localtime(timestamp)
        formatTime = time.strftime("%Y", ftimeArray)
        return formatTime

    def get_hours(self,time_num = time.time()):
        """
        时间戳转为时间格式
        :param time_num: 时间戳
        :return: 时间格式 09:17:30
        """
        return time.strftime('%H:%M:%S',time.localtime(time_num))

    def get_hour(self,time_num = time.time()):
        """
        时间戳转为时间格式
        :param time_num: 时间戳
        :return: 时间格式 09:17:30
        """
        return time.strftime('%H',time.localtime(time_num))

    def get_minutes(self,time_num = time.time()):
        """
        时间戳转为时间格式 分
        :param time_num: 时间戳
        :return: 时间格式 09:17:30
        """
        return time.strftime('%M',time.localtime(time_num))

    def get_seconds(self,time_num = time.time()):
        """
        时间戳转为时间格式 s
        :param time_num: 时间戳
        :return: 时间格式 09:17:30
        """
        return time.strftime('%S',time.localtime(time_num))

    def get_nyrtime(self,time_num = time.time()):
        """
        时间戳转为时间格式 s
        :param time_num: 时间戳
        :return: 时间格式   2023-09-18 09:17:30
        """
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time_num))

    def get_nyr(self,time_num = time.time()):
        """
        时间戳转为时间 2023-09-18
        :param time_num: 时间戳
        :return: 年月日 2023-09-18
        """
        return time.strftime('%Y-%m-%d',time.localtime(time_num))

    def get_logtime(self,time_num = time.time()):
        """
        时间戳转为时间 20230918
        :param time_num: 时间戳
        :return: 年月日 20230918
        """
        return time.strftime('%Y%m%d',time.localtime(time_num))

class MyMath:

    def gdc(self,a ,b):
        """
        求两个数的公约数
        :param a: 数值1
        :param b: 数值2
        :return: 公约数
        """
        if b == 0:
            return a
        return self.gdc(b,a % b)

    def prol(self,a,b):
        """
        求出两个数值的比值
        :param a: 数值1
        :param b: 数值2
        :return: (a:b)
        """
        if b != 0:
            gdc = self.gdc(a,b)
            return (int(a/gdc),int(b/gdc))


getTime = GetTime()
myMath = MyMath()

if __name__ == '__main__':
    print(myMath.gdc(60,9))
    print(myMath.prol(60,9))

    value = getTime.get_time()
    # print(value)
    # value = getTime.get_tiem_int(value)
    # print(value)
    year = getTime.get_hour()
    # print(year)

