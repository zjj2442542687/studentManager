from django.core.cache import cache

# 保存验证码到cache中
from parent.models import Parent
from student.models import Student
from teacher.models import Teacher
from user.models import User
from utils.my_encryption import my_decode_token
from utils.my_response import response_error_400
from utils.status import STATUS_NOT_FOUND_ERROR


def send_code(phone_number: str) -> bool:
    cache.set(f'{phone_number}_code', phone_number[-6:], 600)
    return True


# 从cache中验证验证码
def judge_code(phone_number: str, code: str) -> bool:
    if code:
        return cache.get(f'{phone_number}_code') == code
    return False


# 判断手机号是否存在
def check_phone_number(phone_number) -> bool:
    return User.objects.filter(phone_number=phone_number).exists()


# 判断用户名是否存在
def check_user_name(user_name) -> bool:
    return User.objects.filter(user_name=user_name).exists()


# 根据角色id删除对应的用户
def del_user(role, pk):
    user_id = -1
    # 老师或辅导员
    if role == 0 or role == 3:
        teacher = Teacher.objects.filter(pk=pk)
        if not teacher:
            return response_error_400(status=STATUS_NOT_FOUND_ERROR, message=f"id({pk})未找到")
        user_id = teacher.user_info_id
    # 学生
    elif role == 1:
        student = Student.objects.filter(pk=pk)
        if not student:
            return response_error_400(status=STATUS_NOT_FOUND_ERROR, message=f"id({pk})未找到")
        user_id = student.user_info_id
    # 家长
    elif role == 2:
        parent = Parent.objects.filter(pk=pk)
        if not parent:
            return response_error_400(status=STATUS_NOT_FOUND_ERROR, message=f"id({pk})未找到")
        user_id = parent.user_info_id
    else:
        return response_error_400(status=STATUS_NOT_FOUND_ERROR, message=f"role({role})范围应该在(0`3)")
    if not User.objects.filter(pk=user_id):
        return response_error_400(status=STATUS_NOT_FOUND_ERROR, message=f"role={role}中对应的用户id{user_id}未找到")
    User.objects.get(pk=user_id).delete()
    return None


# 根据token获得详细信息
def get_info_by_token(token):
    dk = my_decode_token(token)
    if not dk:
        return None
    return get_info(int(dk[0]), int(dk[1]))


# 根据用户id和role获得详细信息
def get_info(user_id: int, role: int):
    print(f'userId={user_id}, role={role}')
    # 老师(0) 或 辅导员(3)
    if role == 0 or role == 3:
        try:
            return Teacher.objects.get(user_info_id=user_id)
        except Teacher.DoesNotExist:
            return None
    # 学生
    elif role == 1:
        try:
            return Student.objects.get(user_info_id=user_id)
        except Student.DoesNotExist:
            return None
    # 家长
    elif role == 2:
        try:
            return Parent.objects.get(user_info_id=user_id)
        except Parent.DoesNotExist:
            return None
    elif role == -1:
        return User.objects.get(id=user_id)
    return None
