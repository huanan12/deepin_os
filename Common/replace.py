"""
ReplaceData         数据处理类
repdata             数据替换方法的类方法
set_envs            设置环境变量的类方法
del_envdata         删除环境变量的类方法
get_even            拉取环境变量key对应的值的类方法
"""

import re
import json
import random

from Common.env_data import EnvData
from Common.do_config import conf
from Common.do_path import data_path
from Common.do_excel import DoExcel
from Common.my_logger import logger


class ReplaceData:

    def repdata(self,case,mark = None,real_data = None,num = None):
        """
        :param case: 数据源
        :param mark: 需要替换的原数据   不填：通过正则替换所有
        :param real_data: 替换后的新数据  不填：通过正则替换所有
        :param num: 执行几次替换  不填：全部替换
        :return: 返回替换后的新数据
        """
        # 将传进来的的数据转为字符串
        case_str = json.dumps(case)
        # 将数据进行替换
        if mark != None and real_data != None:
            new_case = self.repdata_all(case,mark,str(real_data),num)
            # 返回的是字典格式，所以无需转换
            case_dict = new_case
        else:
            new_case = self.repdatas(case_str)
            # 将数据重新转为字典格式
            case_dict = json.loads(new_case)
        print(type(case_dict))
        return case_dict

    def repdatas(self,data):
        """
        #(.*?)# 字符自动替换
        :param data: 替换的数据源
        :return: 返回已经替换号的数据
        """
        # 查找需要替换的#(.*?)#
        res = re.findall("#(.*?)#", data)

        # setattr(EnvData,"money","100")
        # 如果查找的为空列表，就不进行替换
        if res:
            # 遍历列表
            for item in res:
                try:
                    # 查找配置文件是否有需要替换的值
                    value = conf.get(conf.get("evment","name"), item)
                except:
                    try:
                        # 配置文件没有找到，去EnvData查找
                        value = getattr(EnvData, item)
                    except AttributeError:
                        # 如果没有找到就不做替换
                        # value = "#{}#".format(item)
                        continue

                # 替换
                data = data.replace("#{}#".format(item), str(value))
                logger.info("替换前的值为:{},替换后的值为：{}".format(item,value))
        return data

    #  忽略repdatass
    def repdatass(self,data,flag = None):
        """
        repdatas备份
        #(.*?)# 字符自动替换
        :param data: 替换的数据源
        :return: 返回已经替换号的数据
        """
        # 查找需要替换的#(.*?)#
        res = re.findall("#(.*?)#", data)

        # setattr(EnvData,"money","100")
        # 如果查找的为空列表，就不进行替换
        if res:
            # 遍历列表
            for item in res:
                if flag:
                    if item == "media":
                        items = item + str(random.randint(1,flag))
                        data = data.replace("#{}#".format(item), "#{}#".format(items),1)
                        item = items
                    elif item == "image":
                        items = item + str(random.randint(1, flag))
                        data = data.replace("#{}#".format(item), "#{}#".format(items),1)
                        item = items

                try:
                    # 查找配置文件是否有需要替换的值
                    value = conf.get(conf.get("evment","name"), item)
                except:
                    try:
                        # 配置文件没有找到，去EnvData查找
                        value = getattr(EnvData, item)
                    except AttributeError:
                        # 如果没有找到就不做替换
                        # value = "#{}#".format(item)
                        continue

                # 替换
                data = data.replace("#{}#".format(item), str(value))
                logger.info("替换前的值为:{},替换后的值为：{}".format(item,value))
        return data

    def set_envs(self,data,mykey = "mykey",valus = "values"):
        """
        :param data: 数据源，操作多条数据
        :param mykey: 环境变量key
        :param valus: 环境变量value
        :return: 返回为空，直接操作设置环境变量
        """
        for i in range(len(data)):
            setattr(EnvData,str(data[i][mykey]),data[i][valus])

    #  忽略set_envdata
    def set_envdata(self,mod ="media",modd = None ):
        media = DoExcel(data_path + r"\api_cases.xlsx", mod)
        medias = media.all_excel()
        if mod.lower() == "media":
            modd = "FMediaId"
        elif mod.lower() == "image":
            modd = "FImageId"

        for i in range(len(medias)):
            title = mod + str(i + 1)
            valuse = medias[i][modd]
            setattr(EnvData,title,valuse)

    def del_envdata(self,flag = None):
        """
        :param flag: 开关  true：用于指定删除某一个EnvData环境变量  false:删除所有EnvData环境变量
        :return:  返回为空，直接操作删除环境变量
        """
        if flag:
            delattr(EnvData,flag)
        else:
            values =dict(EnvData.__dict__.items())
            for key,value in values.items():
                if key.startswith("__"):
                    pass
                else:
                    delattr(EnvData,key)

    def repdata_all(self,case,mark,real_data,num = None):
        """
        case: 数据源
        mark: 需要替换的字符
        real_data: 替换后的字符   real_data替换mark
        """
        # 替换前转为字符串进行处理
        values = json.dumps(case)
        if values is not None and isinstance(values,str):
            # 查找到就进行替换，-1是指查找不到
            if values.find(mark) != -1:
                if num == None:
                    case = values.replace(mark, real_data)
                else:
                    case = values.replace(mark, real_data,num)
        # 返回转为json格式
        case = json.loads(case)
        return case

    def get_even(self,key):
        """
        查找环境变量 优先查找配置文件，未找到接着查找EnvData，还未找到，原样返回
        :param key: 查找的key
        :return: 1.找到key对应的值，返回对应的value 2.没有找到，返回找到的key
        """
        try:
            keys = conf.get(conf.get("evment","name"),key)
        except:
            try:
                keys = getattr(EnvData,key)
            except:
                keys = None
        return keys

replace_data = ReplaceData()


if __name__ == '__main__':
    # from Common.new_phone import new_tol
    # tol = new_tol.check_phone_db()
    # print(tol)
    # case = {'id': 13, 'title': '不输入类型', 'method': 'post', 'url': 'http://api.lemonban.com/futureloan/member/register', 'request_data': '{"mobile_phone":"#phone#","pwd":"12345678"}', 'expected': '{"code":0,"msg":"OK"}', 'check_db': 'select * from member where mobile_phone = "#phone#"'}
    # data = replace_data.repdata(case,"#phone#",str(tol))
    # print(data)

    # oks ={'case_id': 1, 'interface': 'recharge', 'title': '充值成功-整数', 'method': 'post', 'url': 'member/recharge',
    #      'request_data': '{"member_id": #member_id#,"amount":600}',
    #      'expected': '{"code":0,"msg":"OK","data":{"id":#member_id#,"leave_amount":#money#}}',
    #      'check_sql': 'select CAST(member.leave_amount AS CHAR) as leave_amount from member where id=#member_id#;',
    #      'check_sql2': None}
    # rplay = replace_data.repdata_one(oks)
    # print(rplay)

    # setattr(EnvData,"ab","11")
    mod = "media"
    media = DoExcel(data_path + r"\api_cases.xlsx", mod)
    medias = media.all_excel()
    replace_data.set_envs(medias)
    # replace_data.set_envdata()
    # print(getattr(EnvData,"ab"))
    # replace_data.set_envdata("image")
    # replace_data.del_envdata()
    # print(EnvData.__dict__)
    # replace_data.del_envdata("media_1")
    # replace_data.del_envdata("media_2")
    # print(EnvData.__dict__)
    # import random
    # print(random.randint(1,5))

