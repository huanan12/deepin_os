# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2022-04-10 20:39:59
# @Last Modified by:   Administrator
# @Last Modified time: 2022-04-10 20:57:26
"""
读取配置文件


"""

import os
from configparser import ConfigParser

from Common import do_path

class DoConf(ConfigParser):
	def  __init__(self,file_path):
		super().__init__()
		self.file_path = file_path
		self.read(file_path,encoding = "utf-8")

	def save(self):
		super().write(open(self.file_path,"w"))

conf = DoConf(os.path.join(do_path.conf_path,"my_config.ini"))


if __name__ == '__main__':
	values = conf.get("log","name")
	values_1 = conf.get("log","level")

	print(values)
	print(values_1)
