"""
ResponseData        接口返回处理类
res_data            将返回结果某个字段的值设置为环境变量   $.获取接口返回层级目录
my_request          判断环境变量是否有token，有带上token进行请求，如果没有不进行请求
"""

import json
from jsonpath import jsonpath

from Common.env_data import EnvData
from Common.my_logger import logger
from Common.my_requests import chen_request

class ResponseData:
    def res_data(self,excel_data,respons):
        excel_datas = str(excel_data)
        excel_datas = eval(excel_datas)
        logger.info("设置环境变量的键值为:{}".format(excel_datas))
        logger.info("接口返回值为：\n{}".format(respons))
        for key, value in excel_datas.items():
            # 通过$.获取层级目录
            values = jsonpath(respons, value)[0]
            logger.info("设置环境变量{}的值为:{}".format(key, values))
            setattr(EnvData, key, str(values))


    def my_request(self,case):
        case["request_data"] = str(case["request_data"])
        # case["request_data"] = json.loads(case["request_data"])
        case["request_data"] = eval(case["request_data"])
        if hasattr(EnvData,"token"):
            res = chen_request(case["method"],case["url"],case["request_data"],getattr(EnvData,"token"))
        else:
            res = chen_request(case["method"], case["url"], case["request_data"])
        return res

resps = ResponseData()

if __name__ == '__main__':
    excel_data = {'member_id': '$..id', 'token': '$..token'}
    respons = {'code': 0, 'msg': 'OK',
     'data': {'id': 351, 'leave_amount': 0.0, 'mobile_phone': '13208591217', 'reg_name': '美丽可爱的小简',
              'reg_time': '2022-04-28 20:42:19.0', 'type': 0,
              'token_info': {'token_type': 'Bearer', 'expires_in': '2022-04-28 20:47:19',
                             'token': 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjM1MSwiZXhwIjoxNjUxMTUwMDM5fQ.sU3qD2Kyr28t40KUSlI5B2eNrIOrH54A5o6OpF98yuSmBwHTcLM6dCWJeu6TJehcS9FCCnm_nNxdaHe-3rmSfw'}},
     'copyright': 'Copyright 柠檬班 © 2017-2019 湖南省零檬信息技术有限公司 All Rights Reserved'}

    # resps.res_data(excel_data,respons)
    a = jsonpath(respons,"$.data")
    print(a)
    # a = getattr(EnvData,"member_id")
    # token = getattr(EnvData,"token")
    # print(a)
    # print(token)
