import time
from rest_framework.authentication import BaseAuthentication

from user.models import User


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # token = request.data.get("token")
        #
        # user = User.objects.get(token=token)
        print(time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time())))
        # if user_name != 'hhh':
        #     return -1, 0
        return 1, 1
