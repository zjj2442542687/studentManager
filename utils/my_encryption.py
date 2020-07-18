"""
加密解密工具
"""


from django.core import signing


# 加密
def my_encode(value):
    return signing.b64_encode(value.encode()).decode()


# 解密
def my_decode(value):
    return signing.b64_decode(value.encode()).decode()
