import time

from django.db.models import Q

from classs.models import Class
from regular_add_record.models import RegularAddRecord
from student.models import Student
from utils.my_response import response_success_200
from utils.status import STATUS_404_NOT_FOUND, STATUS_NULL, STATUS_TOKEN_NO_AUTHORITY


def check_insert_info(request):
    # 检测id项
    regular_add_record_id = request.data.get("regular_add_record")
    if not regular_add_record_id:
        return response_success_200(code=STATUS_NULL, message="regular_add_record不能为空")
    elif not RegularAddRecord.objects.filter(id=regular_add_record_id):
        return response_success_200(code=STATUS_404_NOT_FOUND, message="regular_add_record没找到该id")

    try:
        # 用户所在班级的id
        clazz = Student.objects.get(user_id=request.user)
        clazz_id = -1
        if clazz:
            clazz_id = clazz.clazz_id
        # 检测用户是否添加了这个打卡项，或者是用户班级添加的
        if not RegularAddRecord.objects.filter(Q(user_id=request.user) | Q(clazz_id=clazz_id),
                                               id=regular_add_record_id):
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="该用户没有添加这个打卡项")
    except Student.DoesNotExist:
        print("没找到学生")
        pass


    # 判断打卡时间段
    time_stamp = time.time()  # 现在的时间段
    # regular_add_record =