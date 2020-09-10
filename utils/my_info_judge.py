import re

from coreapi import exceptions
from rest_framework.response import Response

from user.models import User
from utils.my_response import response_error_400
from utils.status import *

"""
一些信息的验证
"""

# 判断身份证的合法性
def pd_card_3(id_number_str: str) -> bool:
    # 判断长度，如果不是 18 位，直接返回失败
    if len(id_number_str) != 18:
        return False
    id_regex = '[1-9][0-9]{14}([0-9]{2}[0-9X])?'
    if not re.match(id_regex, id_number_str):
        return False
    items = [int(item) for item in id_number_str]
    # 加权因子表
    factors = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    # 计算17位数字各位数字与对应的加权因子的乘积
    copulas = sum([a * b for a, b in zip(factors, items)])
    # 校验码表
    check_codes = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    checkcode = check_codes[copulas % 11].upper()
    return checkcode == id_number_str[-1:]


# 验证身份证的另外一种算法
def pd_card_2(num_str: str) -> bool:
    str_to_int = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10}
    check_dict = {0: '1', 1: '0', 2: 'X', 3: '9', 4: '8', 5: '7',
                  6: '6', 7: '5', 8: '4', 9: '3', 10: '2'}
    if len(num_str) != 18:
        print(u'请输入标准的第二代身份证号码')
        return False
    check_num = 0
    for index, num in enumerate(num_str):
        if index == 17:
            right_code = check_dict.get(check_num % 11)
            if num == right_code:
                print(u"身份证号: %s 校验通过" % num_str)
                return True
            else:
                print(u"身份证号: %s 校验不通过, 正确尾号应该为：%s" % (num_str, right_code))
                return False
        check_num += str_to_int.get(num) * (2 ** (17 - index) % 11)
    return False


# 判断身份证的合法性
def pd_card(card: str) -> bool:
    if not card:
        return False
    regular_expression = "(^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$)|" + \
                         "(^[1-9]\\d{5}\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}$)"
    # 假设18位身份证号码: 41000119910101123

    matches = re.match(regular_expression, card) is not None

    print(matches)
    print(len(card))

    # 判断第18位校验值
    if matches:
        if len(card) == 18:
            try:
                # 前十七位加权因子
                id_card_wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
                # 这是除以11后，可能产生的11位余数对应的验证码
                id_card_y = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]
                s = 0
                for i in range(0, len(id_card_wi)):
                    current = int(card[i:i + 1])
                    s += current * id_card_wi[i]
                id_card_last = card[-1:]
                id_card_mod = s % 11
                if id_card_y[id_card_mod].upper() == id_card_last.upper():
                    return True
                else:
                    return False
            except exceptions:
                print("cwu")
                return False
    return matches


# 判断手机号的合法性
def pd_phone_number(phone) -> bool:
    return re.match(r'^1[345678]\d{9}$', phone) is not None


# 密码复杂度
def pd_password(password: str) -> str:
    # 去掉首尾空格后判断密码长度,
    return None if len(password.strip()) >= 6 else "密码长度需要大于等于6位"


# 判断邮箱
def pd_email(email: str) -> bool:
    s = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    return re.match(s, email) is not None


# 判断qq号
def pd_qq(qq: str) -> bool:
    # s = r'[1-9][0-9]{5,9}'
    s = '[1-9]\d{4,11}$'
    return re.match(s, qq) is not None


# token是否还有效果
def pd_token(request):
    token = request.META.get("HTTP_TOKEN")
    if request.user == STATUS_TOKEN_OVER:
        return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
    elif request.user == STATUS_TOKEN_PARAMETER_ERROR:
        return response_error_400(staus=STATUS_TOKEN_PARAMETER_ERROR, message="token参数错误!!!!!")
    elif not User.objects.filter(token=token):
        return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
    return None


# 检查权限(管理员)
def pd_adm_token(request):
    check_token = pd_token(request)
    if check_token:
        return check_token
    elif request.auth >= 0:
        return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

    return None


# 超级管理员
def pd_super_adm_token(request):
    check_token = pd_token(request)
    if check_token:
        return check_token
    elif request.auth != -1:
        return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="权限不够")

    return None


# 查看权限
def lookup_token(request):
    token = request.META.get("HTTP_TOKEN")
    check_token = pd_token(request)
    if check_token:
        return check_token

    return User.objects.get(token=token).role
    # return request.auth
