from classs.models import Class
from school.models import School
from user.models import User
from user_details.models import UserDetails
from utils.my_response import response_error_400
from utils.status import STATUS_PARAMETER_ERROR


# 检测学生插入信息时数据的合法性
def check_student_insert_info(request):
    school = request.data.get('school')
    clazz = request.data.get('clazz')
    card = request.data.get('card')
    phone_number = request.data.get('phone_number')
    name = request.data.get('name')

    # 不能为空的数据
    if not card:
        return response_error_400(message="card 不能为空")
    if not name:
        return response_error_400(message="card 不能为空")

    # 学校关联
    if not School.objects.filter(id=school):
        return response_error_400(staus=STATUS_PARAMETER_ERROR, message="学校不存在")
    # 班级关联
    if not Class.objects.filter(id=clazz):
        return response_error_400(staus=STATUS_PARAMETER_ERROR, message="班级不存在")
    # 用户检查是否存在
    if UserDetails.objects.filter(card=card):
        return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
    if User.objects.filter(phone_number=phone_number):
        return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")


# 创建userDetails
def create_user_details_and_user():
    pass

