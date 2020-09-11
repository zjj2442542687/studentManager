import time

from django.db.models import Q

from classs.models import Class
from regular_add_record.models import RegularAddRecord
from student.models import Student
from utils.my_response import response_error_400


def check_insert_info(request):
    # 检测id项
    regular_add_record_id = request.data.get("regular_add_record")
    if not regular_add_record_id:
        return response_error_400(message="regular_add_record不能为空")
    elif not RegularAddRecord.objects.filter(id=regular_add_record_id):
        return response_error_400(message="regular_add_record没找到该id")

    # 用户所在班级的id
    clazz = Student.objects.get(user_id=request.user)
    clazz_id = -1
    if clazz:
        clazz_id = clazz.clazz_id
    # 检测用户是否添加了这个打卡项，或者是用户班级添加的
    if not RegularAddRecord.objects.filter(Q(user_id=request.user) | Q(clazz_id=clazz_id), id=regular_add_record_id):
        return response_error_400(message="该用户没有添加这个打卡项")

    # 判断打卡时间段
    time_stamp = time.time()  # 现在的时间段
    # regular_add_record =