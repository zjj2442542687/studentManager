import re

# '"1","2"' 的 字符串转换成 [1, 2] int数组
from classs.models import Class
from regular_category.models import RegularCategory
from school.models import School
from user.models import User


def string_to_int_arr(s: str):
    s = s.split(",")
    s = [int(re.sub("\D", "", w)) for w in s]
    return s


# 获得所有RegularCategory中的id 返回list
def get_regular_category_all_id() -> list:
    regular_category = RegularCategory.objects.all()
    return [r.id for r in regular_category]


# 获得所有user中的id 返回list
def get_user_all_id() -> list:
    user = User.objects.all()
    return [u.id for u in user]


# 获得所有school中的id 返回list
def get_school_all_id() -> list:
    school = School.objects.all()
    return [s.id for s in school]


# 获得所有class中的id 返回list
def get_class_all_id() -> list:
    clazz = Class.objects.all()
    return [c.id for c in clazz]
