import time
from rest_framework.authentication import BaseAuthentication

from user.models import User
from utils.my_encryption import check_token, my_decode_token
from utils.status import STATUS_TOKEN_OVER, STATUS_PARAMETER_ERROR


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        if token and token != '-1':
            try:
                if not token:
                    raise UserWarning
                    # return Response({"message": "有空参数"})
                elif token == -1:
                    # token失效
                    return STATUS_TOKEN_OVER, STATUS_TOKEN_OVER
                else:
                    if check_token(token):
                        ds = my_decode_token(token)
                        pk = ds[0]
                        role = ds[1]
                        return int(pk), int(role)
                    else:
                        # token失效
                        return STATUS_TOKEN_OVER, STATUS_TOKEN_OVER
            except User.DoesNotExist:
                # token失效
                return STATUS_TOKEN_OVER, STATUS_TOKEN_OVER
        #
        # user = User.objects.get(token=token)
        print(time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time())))
        # if user_name != 'hhh':
        #     return -1, 0
        # 参数错误！！！
        return STATUS_PARAMETER_ERROR, STATUS_PARAMETER_ERROR
