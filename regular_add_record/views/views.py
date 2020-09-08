from regular.models import Regular
from regular_category.models import RegularCategory
from user.models import User
from utils.my_response import response_error_400


def check_insert_info(title, regular_category_id, user_id):
    if not title:
        return response_error_400(message="title不能为空")
    if not regular_category_id:
        return response_error_400(message="regular_category不能为空")
    if not user_id:
        return response_error_400(message="user不能为空")

    return check_update_info(regular_category_id, user_id)


# regular_category_id, user_id 不为空则检测他们的合法性
def check_update_info(regular_category_id, user_id, pk=None):
    if regular_category_id:
        if not RegularCategory.objects.filter(id=regular_category_id):
            return response_error_400(message="无效的regular_category")
    if user_id:
        if not User.objects.filter(id=user_id):
            return response_error_400(message="无效的user")
    if pk:
        if not Regular.objects.filter(pk=pk):
            return response_error_400(message="id未找到")
    return None
