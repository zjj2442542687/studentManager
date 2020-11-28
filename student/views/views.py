from classs.models import Class
from school.models import School
from user.models import User
from user_details.models import UserDetails
from utils.my_card import IdCard
from utils.my_encryption import my_encode
from utils.my_info_judge import pd_card, pd_qq, pd_email, pd_phone_number
from utils.my_response import response_success_200
from utils.my_time import date_to_time_stamp
from utils.status import STATUS_PARAMETER_ERROR


# 检测学生插入信息时数据的合法性
def check_student_insert_info(request):
    school = request.data.get('school')
    clazz = request.data.get('clazz')
    card = request.data.get('card')
    phone_number = request.data.get('phone_number')
    name = request.data.get('name')
    qq = request.data.get('qq')
    email = request.data.get('email')

    # 不能为空的数据
    if not card:
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="card 不能为空")
    if not name:
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="name 不能为空")

    # 学校关联
    if not School.objects.filter(id=school):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="学校不存在")
    # 班级关联
    if not Class.objects.filter(id=clazz):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="班级不存在")
    # 用户检查是否存在
    if UserDetails.objects.filter(card=card):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
    if User.objects.filter(phone_number=phone_number):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")

    # 验证格式
    if not pd_card(card):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="身份证格式错误")
    if qq and not pd_qq(qq):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="qq格式不正确")
    if email and not pd_email(email):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="email格式不正确")
    if phone_number and not pd_phone_number(phone_number):
        return response_success_200(code=STATUS_PARAMETER_ERROR, message="手机号格式错误")


# 创建userDetails和user
def create_user_details_and_user(request, role):
    card = request.data.get('card')
    phone_number = request.data.get('phone_number')
    name = request.data.get('name')
    qq = request.data.get('qq')
    email = request.data.get('email')

    # 解析身份证
    id_card = IdCard(card)
    print(id_card.birth_year)
    print(id_card.birth_month)
    print(id_card.birth_day)
    # 创建userDetails
    user_details = UserDetails.objects.create(
        name=name,
        qq=qq,
        email=email,
        sex=id_card.sex,
        card=card,
        birthday=date_to_time_stamp(year=id_card.birth_year, month=id_card.birth_month, day=id_card.birth_day), )

    # 密码为身份证的后6位, 用户名为身份证
    password = my_encode(card[-6:])
    user: User = User.objects.create(user_name=card, password=password, phone_number=phone_number,
                                     role=role, user_details_id=user_details.id)

    # 保存该字段
    request.data["user"] = user.id
