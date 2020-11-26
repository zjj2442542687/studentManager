import datetime
import time

from django.db.models import Q

from classs.models import Class
from regular.models import Regular
from regular_add_record.models import RegularAddRecord
from regular_clock.models import RegularClock
from student.models import Student
from utils.my_response import response_success_200
from utils.my_time import date_to_time_stamp
from utils.status import STATUS_404_NOT_FOUND, STATUS_NULL, STATUS_TOKEN_NO_AUTHORITY, STATUS_EXISTS_ERROR, \
    STATUS_500_INTERNAL_SERVER_ERROR


def check_insert_info(request):
    # 检测id项
    regular_add_record_id = request.data.get("regular_add_record")
    # 打卡的时间戳
    clock_in_time = int(request.data.get("clock_in_time"))
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
        if not Regular.objects.filter(clazz_id=clazz_id) and not RegularAddRecord.objects.filter(user_id=request.user):
            return response_success_200(code=STATUS_TOKEN_NO_AUTHORITY, message="该用户没有添加这个打卡项")
    except Student.DoesNotExist:
        print("没找到学生")
        pass

    # 判断该学生是否今日已经打卡了
    date = datetime.datetime.now()
    # yyyy年MM月dd日 0:0:0
    now = date_to_time_stamp(year=date.year, month=date.month, day=date.day)
    # 第二天
    now2 = now + 24 * 3600

    if clock_in_time < now or clock_in_time > now2:  # 不是今日的打卡
        response_success_200(code=STATUS_500_INTERNAL_SERVER_ERROR, message="签到未开放3")
    if RegularClock.objects.filter(clock_in_time__gte=now, clock_in_time__lt=now2,
                                   regular_add_record_id=regular_add_record_id):
        return response_success_200(code=STATUS_EXISTS_ERROR, message="今日已签到")

    # 判断打卡时间段
    regular_add_record = RegularAddRecord.objects.get(id=regular_add_record_id)
    start_time = time.localtime(regular_add_record.start_time)  # 开始时间的时间戳
    end_time = time.localtime(regular_add_record.end_time)  # 结束时间的时间戳
    start_date = regular_add_record.start_date  # 开始日期的时间戳
    end_date = regular_add_record.end_date  # 结束日期的时间戳
    start_time = date_to_time_stamp(hour=start_time.tm_hour, minute=start_time.tm_min)
    end_time = date_to_time_stamp(hour=end_time.tm_hour, minute=end_time.tm_min)
    now = date_to_time_stamp(hour=date.hour, minute=date.minute)
    if time.time() < start_date or time.time() > end_date:  # 不在这个日期时间段中
        return response_success_200(code=STATUS_500_INTERNAL_SERVER_ERROR, message="签到未开放1")

    if now < start_time or now > end_time:  # 不在这个时间段中
        return response_success_200(code=STATUS_500_INTERNAL_SERVER_ERROR, message="签到未开放2")


