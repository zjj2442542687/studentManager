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
def my_encode_token(username):
    time.time()
    # return signing.b64_encode(value.encode()).decode()


# 解密token
def my_decode_token(token):
    return 0
    # return signing.b64_decode(value.encode()).decode()
