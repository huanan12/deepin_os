# print("ok")
"""
isreq 判断请求参数的合法性

"""
def isreq(req_data, reference):
    """
    判断请求参数的合法性
    :param req_data: req实际请求数据{"name": "jack", "pwd": "123", "tel": "123"}
    :param reference: 所有字段命名{"name": {"name": "name", "type": "str", "required": True},
             "pwd": {"name": "pwd", "type": "str", "required": True},
             "tel": {"name": "tel", "type": "str", "required": True}}
    :return: 返回是否是合法,可以通过code是否为0判断
    """
    # 存储所有字段名：['name', 'pwd', 'tel']
    title_list = []
    # 存储所有类型：['name', 'type', 'required']
    type_list = []
    # 存储所有必填字段名： required为True
    required_list = []
    # 如果传参没问题，默认返回值
    msg = "ok"

    # 存储所有字段名
    for key in reference.keys():
        title_list.append(key)

    # 存储所有类型
    for data in reference.values():
        for key in data.keys():
            if key not in type_list:
                type_list.append(key)

        # 存储所有必填字段名：
        if "required" in type_list and data["required"]:
            required_list.append(data["name"])

    # 存储传参数
    req_title_list = []
    for key in req_data.keys():
        req_title_list.append(key)

    # 判断必填参数
    for isrequired in required_list:
        if isrequired not in req_title_list:
            msg = "缺少必填参数：{}".format(isrequired)
            return {"code":1000,"msg":msg}

    # 判断参数类型
    for key, value in req_data.items():
        if key in title_list:
            types = reference[key]["type"]
            if not isinstance(value, eval(types)):
                msg = "{}传的类型不对，应该传：{}".format(key, types)
                return {"code": 1001, "msg": msg}

    # 如果上面判断都没问题了返回
    return {"code":0,"msg":msg}
if __name__ == '__main__':
    reqs = {"name": "jack", "pwd": "123", "tel": "123"}
    # reqs = {"name": "jack", "pwd": 123}
    # mylog = [{"name":"name","type":"str","required":True},{"name":"pwd","type":"str","required":True},{"name":"tel","type":"str","required":True}]
    mylog = {"name": {"name": "name", "type": "str", "required": True},
             "pwd": {"name": "pwd", "type": "str", "required": True},
             "tel": {"name": "tel", "type": "str", "required": True}}
    title_name = ["name", "type", "required"]

    value = isreq(reqs, mylog)
    print(value)
