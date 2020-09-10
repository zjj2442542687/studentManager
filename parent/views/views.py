from school.models import School
from user.models import User
from user_details.models import UserDetails
from utils.my_info_judge import pd_card, pd_qq, pd_email, pd_phone_number
from utils.my_response import response_error_400
from utils.status import STATUS_PARAMETER_ERROR


# 检测家长插入信息时数据的合法性
def check_parent_insert_info(request):
    card = request.data.get('card')
    phone_number = request.data.get('phone_number')
    name = request.data.get('name')
    qq = request.data.get('qq')
    email = request.data.get('email')

    # 不能为空的数据
    if not card:
        return response_error_400(message="card 不能为空")
    if not name:
        return response_error_400(message="name 不能为空")
    if not phone_number:
        return response_error_400(message="手机号 不能为空")

    # 用户检查是否存在
    if UserDetails.objects.filter(card=card):
        return response_error_400(staus=STATUS_PARAMETER_ERROR, message="身份证已经注册存在")
    if User.objects.filter(phone_number=phone_number):
        return response_error_400(staus=STATUS_PARAMETER_ERROR, message="手机号码已经注册存在")

    # 验证格式
    if not pd_card(card):
        return response_error_400(message="身份证格式错误")
    if qq and not pd_qq(qq):
        return response_error_400(message="qq格式不正确")
    if email and not pd_email(email):
        return response_error_400(message="email格式不正确")
    if not pd_phone_number(phone_number):
        return response_error_400(message="手机号格式错误")
