from regular_add_record.models import RegularAddRecord
from utils.my_encryption import get_time
from utils.my_response import response_success_200
from utils.my_time import date_to_time_stamp, check_time_stamp


def check_authority(self, request, pk):  # 检查权限问题
    if not self.queryset.filter(pk=pk):
        return response_success_200(message="id未找到")

    # 管理员的记录不能被别人删除，其他用户的只能自己删除
    regular_add_record_user = self.queryset.get(pk=pk).user
    regular_add_record_user_id = regular_add_record_user.id
    regular_add_record_user_role = regular_add_record_user.role
    if regular_add_record_user_id != request.user:  # 不是自己的
        if regular_add_record_user_role >= 0:  # 需要删除的regularAddRecord是普通用户的
            if request.auth >= 0:  # 执行的用户是普通用户
                return response_success_200(message="没有权限删除别人的东西!!!")
        else:  # 需要被删除的regularAddRecord是管理员的
            return response_success_200(message="不能删除管理员的东西!!!")


def check_insert_time(request):  # 检查添加数据时，时间的规范
    data = request.data
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not (start_time and end_time and start_date and end_date):
        return response_success_200(message="有空数据")

    # 检测时间的范围

    check_t = check_time(start_time, end_time,
                         minute=3, err_message="结束时间需要大于开始时间3分钟")
    if check_t:
        return check_t

    check_date = check_time(start_date, end_date,
                            minute=30, err_message="结束日期需要大于开始日期30分钟")

    if check_date:
        return check_date


# 检测时间的范围
def check_time_range(time_stamp):
    message = check_time_stamp(time_stamp)
    if message:
        return response_success_200(message=message)


def check_time(start, end, day=0, hour=0, minute=0, second=0, err_message="结束时间需要大于开始时间3分钟"):
    if not (start and end):
        return None
    check = check_time_range(start) or check_time_range(end)
    if check:
        return check

    # 检测开始时间和结束时间之间的相距时间是否符合
    return response_success_200(message=err_message) \
        if start + get_time(day=day, hour=hour, minute=minute, second=second) > end \
        else None


def check_update_time(request, pk):  # 检查修改数据时，时间的规范
    data = request.data
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # 获得pk对应的 对象
    regular_add_record = RegularAddRecord.objects.get(pk=pk)

    check_t = check_time(start_time or regular_add_record.start_time, end_time or regular_add_record.end_time,
                         minute=3, err_message="结束时间需要大于开始时间3分钟")
    if check_t:
        return check_t

    check_date = check_time(start_date or regular_add_record.start_date, end_date or regular_add_record.end_date,
                            minute=30, err_message="结束日期需要大于开始日期30分钟")

    if check_date:
        return check_date
