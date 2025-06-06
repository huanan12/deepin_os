# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2022-03-13 21:02:20
# @Last Modified by:   Administrator
# @Last Modified time: 2022-04-10 22:44:08
"""
路径配置
file_path        获取当前文件路径
tools_path        Common、工具类目录
root_path        工程目录（根目录）
conf_path        配置文件目录
logs_path       日志目录
reports_path    生成报告目录
case_path       测试用例目录
data_path       测试数据目录
temporary_path  temporary临时目录
"""

import os

file_path = os.path.abspath(__file__)

# 工具类目录
tools_path = os.path.dirname(file_path)

# 根目录
root_path = os.path.dirname(tools_path)

# 配置文件目录
conf_path = os.path.join(root_path,"Conf")

# 日志目录
logs_path = os.path.join(os.path.join(root_path,"Outputs"),"logs")

# 生成报告目录
reports_path = os.path.join(os.path.join(root_path,"Outputs"),"reports")

# 测试用例目录
case_path = os.path.join(root_path,"TestCases")

# 测试数据目录
data_path = os.path.join(root_path,"TestDatas")

# temporary临时目录
temporary_path = os.path.join(root_path,"temporary")


