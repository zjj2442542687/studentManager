from django.core.cache import cache

# 保存验证码到cache中
from user.models import User
from user_details.models import UserDetails
from parent.models import Parent
from teacher.models import Teacher
from student.models import Student


def create_user_details(**kwargs) -> bool:
    UserDetails.objects.create(**kwargs)
    return True


def create_parent(**kwargs) -> bool:
    Parent.objects.create(**kwargs)
    return True


def create_teacher(**kwargs) -> bool:
    Teacher.objects.create(**kwargs)
    return True


def create_student(**kwargs) -> bool:
    Student.objects.create(**kwargs)
    return True
