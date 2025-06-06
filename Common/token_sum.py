"""
token 加密，反解析判断

sumTokens：计算token

checkToken ：判断token是否合法

"""

import base64
import hashlib
import time

from Common.do_config import conf


class Token:
    def sumTokens(self, appid, secret, times=None):
        """
        token加密
        :param appid: 应用id
        :param secret: 密钥
        :param times: 时间戳，不传默认当前时间
        :return: 计算的token
        """
        if times:
            T = times
        else:
            T = str(time.time())
        sign = appid + secret + str(T)
        sign = hashlib.sha1(sign.encode("utf-8"))
        sign = sign.hexdigest()
        token = appid + ',' + str(T) + ',' + sign
        # base64加密
        token = base64.b64encode(token.encode("utf-8"))
        # 将字节序列解码为指定编码格式的字符串
        token = token.decode()
        return (token)

    def checkToken(self, tokens, td=20):
        """
        判断传入的token是否合法，时间是否过期，默认20分钟过期
        :param tokens: 传入的token
        :param td: 过期时间
        :return: 一致返回 True  不一致，时间过期返回 Flase
        """
        # 将字符串转换为指定编码格式的字节
        token = tokens.encode()
        # base64解密
        token = base64.b64decode(token).decode()
        # print(token)
        # 将字符串按照,进行切割成数组
        sign = token.split(',')
        # print(sign)
        # 提取appid
        appid = sign[0]
        # 提取token中时间
        T_new = eval(sign[1])
        # 提取加密的sign
        sign_new = sign[2]

        # 拉取配置文件中所有的appid
        token_conf = conf.options("appid")
        # 判断计算的appid是否存在,不存在返回False
        if appid not in token_conf:
            return False

        # 计算时间差，用于算过期时间（分钟）
        s = time.time() - T_new
        sd = s / 60
        # print(sd)

        # 判断时间是否过期，过期返回Flase
        if sd > td and sd < 0:
            return False

        secret = conf.get("appid",appid)

        # print(appid, secret, T_new)

        # 通过解析出来appid和时间，拉取配置中secret值，计算出token
        token_new = self.sumTokens(appid, secret, T_new)
        # print(token_new)

        # 判断传入的token与计算出的token是否一致
        if tokens == token_new:
            return True
        else:
            return False

if __name__ == '__main__':
    mytoken = Token()
    tokens = conf.options("appid")
    appid = tokens[0]
    secret = conf.get("appid",appid)
    c = mytoken.sumTokens(appid,secret)
    d = conf.options("appid")
    d = mytoken.checkToken(c)
    print(c)
    print(d)