# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2022-03-20 21:01:19
# @Last Modified by:   Administrator
# @Last Modified time: 2022-04-12 00:06:07
"""
Mylogger            日志函数封装
console_ok          控制台输出   配置文件 ture：输出  false：不输出
file_ok            文件输出   配置文件 ture：输出  false：不输出
"""

import logging
import os
import time

from Common.do_config import conf
from Common import do_path
from Common.mytime import getTime

class Mylogger(logging.Logger):
    def __init__(self,name,lever = logging.INFO,file = None):
        super().__init__(name,lever)


        # 设置渠道的输出内容格式
        fmt = '%(asctime)s %(name)s %(levelname)s %(filename)s-%(lineno)d行: %(message)s'
        formatter = logging.Formatter(fmt)

        # 控制台输出
        if conf.getboolean("log","console_ok"):
            handle1 = logging.StreamHandler()   # 控制台输出
            handle1.setFormatter(formatter)
            self.addHandler(handle1)

        #文件渠道
        if conf.getboolean("log","file_ok"):
            handles = logging.FileHandler(file,encoding="utf-8")     # 文件输出
            handles.setFormatter(formatter)
            self.addHandler(handles)

    def outlog(self,appid=None,secret=None,token =None,req_url = None,method =None,req_headers=None,req_body=None,status=None,costtime=None,resp_headers=None,resp_body=None):
        outlog_dict = {}
        appid = appid
        outlog_dict["appid"] = appid
        secret = secret
        outlog_dict["secret"] = secret
        token = token
        outlog_dict["token"] = token
        req_url = req_url
        outlog_dict["req_url"] = req_url
        method = method
        outlog_dict["method"] = method
        req_headers = req_headers
        outlog_dict["req_headers"] = req_headers
        req_body = req_body
        outlog_dict["req_body"] = req_body
        status = status
        outlog_dict["status"] = status
        costtime = costtime
        outlog_dict["costtime"] = costtime
        resp_headers = resp_headers
        outlog_dict["resp_headers"] = resp_headers
        resp_body = resp_body
        outlog_dict["resp_body"] = resp_body

        outlog = "\nappid的值：{}\nsecret的值：{}\ntoken的值为：{}\n请求地址：{}\n请求方法：{}\n请求头：{}\n请求体：{}\n响应状态码：{}\n接口耗时：{}\n响应头：{}\n响应体：{}\n".format(appid,secret,token,req_url,method,req_headers,req_body,status,costtime,resp_headers,resp_body)
        return outlog



# getTime.get_logtime(time.time())   #获取当前日期
file_path = os.path.join(do_path.logs_path,getTime.get_logtime(time.time()))

# 判断路径是否存在，不存在新建路径
if os.path.exists(file_path) == False:
    os.mkdir(file_path)
logename = os.path.join(file_path,conf.get("log","file_name"))

# 使用直接调用logger，不用实例化
logger = Mylogger(conf.get("log","name"),conf.get("log","level"),logename)



if __name__ == '__main__':
    logger.info("goto")
    logger.warning("goto")

