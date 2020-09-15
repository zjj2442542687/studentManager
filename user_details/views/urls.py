from django.core.cache import cache

# 保存验证码到cache中
from user.models import User
from user_details.models import UserDetails
from utils.my_info_judge import pd_phone_number, pd_card, pd_qq, pd_email
from utils.my_response import response_error_400
from utils.my_time import check_time_stamp


def create_user_details(**kwargs) -> bool:
    UserDetails.objects.create(**kwargs)
    return True


# 管理员修改角色的信息
def adm_update_user_details(user_update:User, request):
    phone_number = request.data.get("phone_number")
    if phone_number:
        if not pd_phone_number(phone_number):
            return response_error_400(message="手机号输入有误")
        if User.objects.exclude(pk=user_update.id).filter(phone_number=phone_number):
            return response_error_400(message="手机号已存在")
        user_update.phone_number = phone_number

    # 获得传过来的参数
    user_details = request.data.get('user_details')
    print(user_details)
    # 获得需要修改的userDetails
    user_detail_update = user_update.user_details
    sex = user_details.get('sex')
    name = user_details.get('name')
    birthday = user_details.get('birthday')
    card = user_details.get('card')
    qq = user_details.get('qq')
    email = user_details.get('email')

    if sex:
        user_detail_update.sex = sex
    if name:
        user_detail_update.name = name
    if birthday:
        check_time = check_time_stamp(int(birthday))
        print(check_time)
        if check_time:
            return response_error_400(message=check_time)
        user_detail_update.birthday = birthday
    if card:
        if not pd_card(card):
            return response_error_400(message="身份证输入有误")
        if UserDetails.objects.exclude(pk=user_detail_update.id).filter(card=card):
            return response_error_400(message="身份证已存在")
        user_detail_update.card = card
    if qq:
        if not pd_qq(qq):
            return response_error_400(message="qq输入有误")
        if UserDetails.objects.exclude(pk=user_detail_update.id).filter(qq=qq):
            return response_error_400(message="qq已存在")
        user_detail_update.qq = qq
    if email:
        if not pd_email(email):
            return response_error_400(message="email输入有误")
        if UserDetails.objects.exclude(pk=user_detail_update.id).filter(email=email):
            return response_error_400(message="email已存在")
        user_detail_update.email = email

    # 保存修改
    user_update.save()
    user_detail_update.save()