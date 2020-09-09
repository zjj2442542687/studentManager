from classs.models import Class
from regular.models import Regular
from regular_category.models import RegularCategory
from user.models import User
from utils.my_info_judge import pd_token
from utils.my_response import response_error_400


def check_insert_info(title, regular_category_id, user_id, class_id):
    if not title:
        return response_error_400(message="title不能为空")
    if not regular_category_id:
        return response_error_400(message="regular_category不能为空")
    if not user_id:
        return response_error_400(message="user不能为空")

    return check_update_info(regular_category_id, user_id, class_id=class_id)


# regular_category_id, user_id 不为空则检测他们的合法性
def check_update_info(regular_category_id, user_id, class_id=None, pk=None):
    if regular_category_id:
        if not RegularCategory.objects.filter(id=regular_category_id):
            return response_error_400(message="无效的regular_category")
    if user_id:
        if not User.objects.filter(id=user_id):
            return response_error_400(message="无效的user")
    if pk:
        if not Regular.objects.filter(pk=pk):
            return response_error_400(message="id未找到")
    if class_id:
        if not Class.objects.filter(id=class_id):
            return response_error_400(message="class_id未找到")
    return None


# 检测用户对这个id的访问权限
def check_pk_and_permission(request, pk):
    if pk:
        if not Regular.objects.filter(pk=pk):
            return response_error_400(message="id未找到")

    check_token = pd_token(request)
    if check_token:
        return check_token

    if request.auth >= 0:  # 普通用户
        if not Regular.objects.filter(user_id=request.user, id=pk):
            return response_error_400(message="没有访问权限!!!!!!!!!!!!!!!!!!!!!")
