from django.core.cache import cache

# 保存验证码到cache中
from user.models import User
from user_details.models import UserDetails


def create_user_details(user_id: int) -> bool:
    UserDetails.objects.create(user_id=user_id)
    return True
