# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2022-04-09 23:14:56
# @Last Modified by:   Administrator
# @Last Modified time: 2022-04-13 00:07:39
""""
请求的封装
chen_request 中台接口请求封装
api_request  api接口请求封装
chagemd5	md5更改
filemd5		md5读取
"""

# 封装requests
import logging
import random

import requests
import json
import base64
import hashlib
import time

from Common.my_logger import logger
from Common.do_config import conf

def __handle_headerl(token = None):
	"""
		__handle_haeaderl  私有函数，获取请求头
		token   token授权
		header   请求头
	"""
	header = {"Content-Type": "application/json"}

	# 判断请求头是否携带token，传入token就写入请求头中
	if token:
		# token = __tokens(token)
		token = tokens(token)
		header["x-tacc-token"] = "{}".format(token)
		# header["spid"] = "{}".format("token")
		logger.info("token： {}".format(token))
	return header

def __tokens(token):
	if token.lower() == "ml_token":
		app = "ml_token"
		sect = "ml_value"
		return __tokensum(app,sect)
	elif token.lower() == "tacc_token":
		app = "tacc_token"
		sect = "tacc_value"
		return __tokensum(app, sect)
	elif token.lower() == "mp_token":
		app = "mp_token"
		sect = "mp_value"
		return __tokensum(app, sect)
	elif token.lower() == "cms_token":
		app = "cms_token"
		sect = "cms_value"
		return __tokensum(app, sect)
	elif token:
		return token
	else:
		logger.info("传入的token不正确，请重新传入，token值为：{}".format(token))

def tokens(token):
	if token.lower() == "ml_token":
		app = "ml_token"
		sect = "ml_value"
		return __tokensum(app,sect)
	elif token.lower() == "tacc_token":
		app = "tacc_token"
		sect = "tacc_value"
		return __tokensum(app, sect)
	elif token.lower() == "mp_token":
		app = "mp_token"
		sect = "mp_value"
		return __tokensum(app, sect)
	elif token.lower() == "cms_token":
		app = "cms_token"
		sect = "cms_value"
		return __tokensum(app, sect)
	elif token:
		return token
	else:
		logger.info("传入的token不正确，请重新传入，token值为：{}".format(token))

def __tokensum(app,sect):
	T = int(time.time())
	mytoken = conf.get("evment","name")
	appid = conf.get(mytoken,app)
	logger.info("appid的值：{}".format(appid))
	secret = conf.get(mytoken,sect)
	logger.info("secret的值：{}".format(secret))
	sign = appid + secret + str(T)
	sign = hashlib.sha1(sign.encode("utf-8"))
	sign = sign.hexdigest()
	token = appid + ',' + str(T) + ',' + sign
	token = base64.b64encode(token.encode("utf-8"))
	token = token.decode()
	logger.info("token的值为：{}".format(token))
	return token


def __base_url(url):
	server = conf.get("evment","name")
	if url.startswith("http"):
		url = url
	elif url.startswith("/"):
		url =conf.get(server,"base_url") + url
	else:
		url =conf.get(server,"base_url") + "/" + url

	return url


def chen_request(modthod,url,datas = None,token = None,file = None):
	"""
		chen_request    自定义请求函数
		modthod		请求方法 例如:get,post
		url 		请求地址
		datas		请求体
		token 		是否token授权
	"""

	# 获取请求头
	header = __handle_headerl(token)
	if file != None:
		del header["Content-Type"]
	url = __base_url(url)

	logger.info("请求地址: {}".format(url))
	logger.info("请求方法： {}".format(modthod))
	logger.info("请求头： {}".format(header))
	logger.info("请求体： {}".format(datas))

	# 将请求方法转为大写
	modthod = modthod.upper()
	# 判断是get请求还是post请求
	if modthod == "GET":
		res = requests.get(url,data = datas,headers = header)
	elif modthod == "POST":
		if file != None:
			res = requests.post(url, data=datas, files=file, headers=header)
		else:
			res = requests.post(url,data = datas,headers = header)
	elif modthod == "PATCH":
		res = requests.patch(url,data = datas,headers = header)

	logger.info("响应状态码: {}".format(res.status_code))
	logger.info("接口耗时ms: {}ms".format((res.elapsed.total_seconds() * 1000)))
	logger.info("接口耗时s: {}s".format(res.elapsed.total_seconds()))
	logger.info("响应头: {}".format(res.headers))
	logger.info("响应体: {}".format(res.json()))
	# 返回请求
	return res

def chen_request_res(modthod,url,datas = None,token = None,file = None):
	"""
		chen_request    自定义请求函数
		modthod		请求方法 例如:get,post
		url 		请求地址
		datas		请求体
		token 		是否token授权
	"""

	# 获取请求头
	header = __handle_headerl(token)
	del header["Content-Type"]
	# header["Content-Type"] = "multipart/form-data"
	url = __base_url(url)

	logger.info("请求地址: {}".format(url))
	logger.info("请求方法： {}".format(modthod))
	logger.info("请求头： {}".format(header))
	logger.info("请求体： {}".format(datas))

	# 将请求方法转为大写
	modthod = modthod.upper()
	# 判断是get请求还是post请求
	if modthod == "GET":
		res = requests.get(url,data = datas,headers = header)
	elif modthod == "POST":
		res = requests.post(url,data = datas,files=file,headers=header)
	elif modthod == "PATCH":
		res = requests.patch(url,data = datas,headers = header)

	logger.info("响应状态码: {}".format(res.status_code))
	logger.info("接口耗时ms: {}ms".format((res.elapsed.total_seconds() * 1000)))
	logger.info("接口耗时s: {}s".format(res.elapsed.total_seconds()))
	logger.info("响应头: {}".format(res.headers))
	logger.info("响应体: {}".format(res.json()))
	# 返回请求
	return res

def api_request(modthod,url,datas = None,para = None,file= None,header = None):
	# 将请求方法转为大写
	modthod = modthod.upper()
	# if para.upper() == "OK":
	# 	para = eval(conf.get(conf.get("evment", "mktapi"), "params"))
	# 判断是get请求还是post请求
	if modthod == "GET":
		res = requests.get(url,params=para, data=datas, headers=header)
	elif modthod == "POST":
		res = requests.post(url,params=para,data=datas,files = file,headers=header)
	elif modthod == "PATCH":
		res = requests.patch(url, data=datas, headers=header)

	logger.info("响应状态码: {}".format(res.status_code))
	logger.info("接口耗时ms: {}ms".format((res.elapsed.total_seconds()*1000)))
	logger.info("接口耗时s: {}s".format(res.elapsed.total_seconds()))
	logger.info("响应头: {}".format(res.headers))
	logger.info("响应体: {}".format(res.json()))
	# 返回请求
	return res

def chagemd5(file_path):
	# 改变文件的MD5
	# filename 文件路径
	myfile = open(file_path, 'a')
	myfile.write("####&&&&")
	myfile.close

def filemd5(file_path,flag = False):
	"""
	读取文件MD5
	:param filename: 路径
	:param flag: 开关 True 改变MD5  False 不改变MD5 只读取MD5
	:return:返回MD5
	"""

	if flag:
		chagemd5(file_path)
	hasher = hashlib.md5()
	with open(file_path, "rb") as file:
		buf = file.read()
		while len(buf) > 0:
			hasher.update(buf)
			buf = file.read()
	return hasher.hexdigest()



if __name__ == '__main__':
	# url = "/material-library/image/get_image_list"
	# data ={"uid":17028362,"offset":0,"limit":10,"order_by":[{"field":"image_id","order":"DESCENDING"}],"need_grant":3,"image_id_list":["3039228818","52434347859"],"uid_list":["95918","17028362"]}
	# datas = json.dumps(data)
	# token = "ml_token"
	# res = chen_request("post",url,datas,token)
	# print(res.json())

	# from Common.do_excel import DoExcel
	# from Common.do_config import conf
	# from Common.do_path import data_path
	# doexcel = DoExcel(data_path + conf.get("excel","name"),"get_image_list")
	# datas = doexcel.all_excel()
	# for i in range(len(datas)):
	# 	# datas[i] = json.dumps(datas[i])
	# 	data = datas[i]["request_data"]
	# 	method = datas[i]["method"]
	# 	url = datas[i]['url']
	# 	token = datas[i]["token"]
	# 	res = chen_request(method, url, data, token)
	# 	print(res.json())

	# 视频上传
	url = conf.get(conf.get("evment","mktapi"),"url") + r"/videos/add"
	modthod = "post"
	file_path = r"D:\大创意\视频\正常时长\case1\16-9\微信\1280-720\ads_svp_video__0b53jaaocaaafyabzcammrrbusae4feabyka.f0.mp4"
	data = {
    "account_id": 25610,
    "signature": "b63dba8cb55da55fcd329886bfb67fc2",
    "description": "ghua1670549809",
}

	# Md5 = filemd5(file_path,True)
	Md5 = filemd5(file_path)
	data["signature"] = Md5
	print(Md5)

	files ={
	"video_file" : open(file_path, "rb")
	}

	par = eval(conf.get(conf.get("evment","mktapi"),"params"))
	res = api_request(modthod,url,data,"ok",files)
	print(res.json())

	# 图片上传
	url = conf.get(conf.get("evment", "mktapi"), "url") + r"/images/add"
	modthod = "post"
	file_path = r"D:\photo\3D_inpainting_test_set\720_1280\0_3527.jpg"
	data = {
    "upload_type": "UPLOAD_TYPE_FILE",
    "account_id": 25610,
    "signature": "1d1fbbeac7f13dbaa03c08fc15bb8629",
    "description": "ghuatest1670570946"
	}

	Md5 = filemd5(file_path)
	data["signature"] = Md5

	files = {
		"file": open(file_path, "rb")
	}
	par = eval(conf.get(conf.get("evment", "mktapi"), "params"))
	res = api_request(modthod, url, data, "ok", files)
	print(res.json())

