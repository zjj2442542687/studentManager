import time
from rest_framework.authentication import BaseAuthentication

from user.models import User
from utils.my_encryption import check_token, my_decode_token


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        if token and token != '-1':
            if check_token(token):
                pk = my_decode_token(token)[0]
                return int(pk), 1
        #
        # user = User.objects.get(token=token)
        print(time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time())))
        # if user_name != 'hhh':
        #     return -1, 0
        return -1, -1
