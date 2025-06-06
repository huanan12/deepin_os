import logging

from Common.pythonhua import MyDb
from Common.is_req import isreq
# from flask import Flask
# from flask_restful import reqparse,abort,Api,Resource
from flask import Flask,request as req

# 实例化app
app = Flask(__name__)

# 设置响应头解决跨域问题
@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/table/get',methods=["GET"])
def get():
    my_db = MyDb()
    table_dict = {}
    databas = my_db.database_where(my_db.database_name())
    for values in databas:
        tables = my_db.tabale_name(values)
        table_dict[values] = tables
    # name = req.json
    name = req.headers
    # name = req.url
    #
    # print(name)
    my_db.close()
    return table_dict

@app.route('/table/desc',methods=["post"])
def tab_desc():
    reqBody = req.json
    database = reqBody["database"]
    table = reqBody["table"]
    # print(reqBody,database,table)
    my_db = MyDb()
    table_dict = {}
    table_desc = my_db.tabale_desc(table,database)
    table_title = my_db.tabale_title(table_desc)
    # print(table_title)
    # name = req.json
    # print(name)
    # name = req.headers
    # name = req.url
    datas = {}
    datas["data"] = table_title
    my_db.close()
    return datas

@app.route('/table/value',methods=["post"])
def tab_value():
    reqBody = req.json
    keys = reqBody["key"]
    wheres = reqBody["value"]
    database_name = reqBody["database_name"]
    table_name = reqBody["table_name"]

    print(keys,wheres)
    my_db = MyDb()

    if keys == {}:
        select_value = my_db.select_all(keys,table_name,database_name)
    else:
        where_list = []
        # [{"field": "id", "operator": ">", "value": 1}, {"field": "name", "operator": "=", "value": "jake"}]
        for key,value in wheres.items():
            where_dict = {}
            where_dict["field"] = key
            where_dict["operator"] = "="
            where_dict["value"] = value
            where_list.append(where_dict)
        select_value = my_db.select_where_all(where_list,keys,table_name,database_name)
    datas = {}
    datas["type_list"] = keys
    datas["data"] = select_value
    print(select_value)
    my_db.close()
    return datas




@app.route('/add',methods=["POST"])
def post():
    my_db = MyDb()
    table_dict = {}
    databas = my_db.database_where(my_db.database_name())
    for values in databas:
        tables = my_db.tabale_name(values)
        table_dict[values] = tables
    reqBody = req.json
    print(reqBody)
    print(table_dict)
    my_db.close()
    return reqBody

# @app.route('/login', methods=["GET","POST"])
# def login():
#
#     res = make_response("login fail") # 设置响应体
#     res.status = '999 login fail' # 设置状态码
#     res.headers['token'] = "123456" # 设置响应头
#     res.headers['City'] = "shenzhen" # 设置响应头
#
#     return res

@app.route('/mylogin', methods=["GET","POST"])
def mylogin():
    # 接口参数文档 name:字段名  type:数据类型   required:是否必填,True 必填,False非必填
    mylogin_req = {"name": {"name": "name", "type": "str", "required": True},
             "pwd": {"name": "pwd", "type": "str", "required": True},
             "tel": {"name": "tel", "type": "str", "required": True}}

    # 获取传参
    req_body = req.json
    # 判断传参是否合法
    value_data = isreq(req_body,mylogin_req)
    if value_data["code"] != 0:
        return value_data

    datas = []
    name = req_body["name"]
    datas.append(req_body)
    my_db = MyDb()
    table_names = "stuname"
    erro_sql = my_db.table_insert(datas,table_names)
    print(erro_sql)
    select_parameter = ["id","name","pwd","tel"]
    wheres = [{"field": "name", "operator": "=", "value": name}]
    res = my_db.select_where_all(wheres,select_parameter,table_names)
    totality = len(res)
    resbody = {"data":res,"totality":totality,"code":0,"msg":"ok"}
    my_db.close()
    return resbody

if __name__ == '__main__':
    app.run(debug= True)
    # app.run(host='0.0.0.0',port=8080)