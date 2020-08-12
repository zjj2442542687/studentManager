"""
加密解密工具
"""
import time

from django.core import signing


# 加密
def my_encode(value):
    return signing.b64_encode(value.encode()).decode()


# 解密
def my_decode(value):
    return signing.b64_decode(value.encode()).decode()


# 加密token
def my_encode_token(pk, role, password):
    # id+空格+role+空格+password+空格+时间进行加密
    return signing.b64_encode((str(pk) + " " + str(role) + " " + password + " " + str(time.time())).encode()).decode()


# 解密token(返回id,role和时间)
def my_decode_token(token):
    try:
        strs = my_decode(token).split()
        return [strs[0], strs[1], strs[-1]]
    except UnicodeDecodeError:
        return None
    # return signing.b64_decode(value.encode()).decode()


# 转换成秒
def get_time(day=0, hour=0, minute=0, second=0):
    return day * (60 * 60 * 24) + hour * (60 * 60) + minute * 60 + second


# token 3天后过期
expiration_time = get_time(day=3)


# 检测token是否过期(true没过期,false过期)
def check_token(token) -> bool:
    if not my_decode_token(token):
        return False
    return time.time() - float(my_decode_token(token)[-1]) <= expiration_time
