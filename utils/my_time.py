import time


# 传入年月日返回时间戳
def date_to_time_stamp(year=2000, month=1, day=1, hour=0, minute=0, second=0, date_format="%Y-%m-%d %H:%M:%S"):
    # 转换成时间数组
    time_array = time.strptime(f'{year}-{month}-{day} {hour}:{minute}:{second}', date_format)
    # 转换成时间戳
    timestamp = time.mktime(time_array)
    return timestamp


# 传入时间戳，返回string
def time_stamp_to_str(time_stamp=time.time(), date_format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(date_format, time.localtime(time_stamp))


# 数据库保存的时间最小的取值
def get_min_time_stamp():
    return date_to_time_stamp(year=1910)


# 数据库保存的时间最大的取值
def get_max_time_stamp():
    return date_to_time_stamp(year=2050)


# 检测时间戳是否在范围内
def check_time_stamp(time_stamp):
    if time_stamp < get_min_time_stamp():
        return f"输入的时间戳需要在1910年({date_to_time_stamp(year=1910)})之后"
    if time_stamp > get_max_time_stamp():
        return f"输入的时间戳需要在2100年({date_to_time_stamp(year=2100)})之前"
