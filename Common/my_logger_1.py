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

class Mylogger(logging.Logger):
    def __init__(self,name,lever = logging.INFO,file = None):
        super().__init__(name,lever)


        # 设置渠道的输出内容格式
        fmt = '%(asctime)s %(name)s %(levelname)s %(filename)s-%(lineno)d行: %(message)s'
        formatter = logging.Formatter(fmt)

        # 控制台输出
        if True:
            handle1 = logging.StreamHandler()   # 控制台输出
            handle1.setFormatter(formatter)
            self.addHandler(handle1)

        #文件渠道
        if True:
            handles = logging.FileHandler(file,encoding="utf-8")     # 文件输出
            handles.setFormatter(formatter)
            self.addHandler(handles)

# 输出日志路径
file_path = "D:\loging"

# 判断路径是否存在，不存在新建路径
if os.path.exists(file_path) == False:
    os.mkdir(file_path)
logename = os.path.join(file_path,"log")

# 使用直接调用logger，不用实例化
logger = Mylogger("log","INFO",logename)



if __name__ == '__main__':
    logger.info("goto")
    logger.warning("goto")
