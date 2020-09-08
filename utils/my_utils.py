import re


# '"1","2"' 的 字符串转换成 [1, 2] int数组
def string_to_int_arr(s: str):
    s = s.split(",")
    s = [int(re.sub("\D", "", w)) for w in s]
    return s
