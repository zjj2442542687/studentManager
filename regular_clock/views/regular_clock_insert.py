from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from regular_clock.models import RegularClock
from regular_clock.views.regular_clock_serializers import RegularClockInfoSerializersAll
from regular_clock.views.views import check_insert_info
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200
from utils.my_utils import get_regular_add_record_all_id


class RegularClockInsertView(mixins.CreateModelMixin,
                             GenericViewSet):
    queryset = RegularClock.objects.all()
    serializer_class = RegularClockInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="添加数据 ",
        manual_parameters=[
            openapi.Parameter('regular_add_record', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='regular_add_record的id，你要给哪个打卡', required=True,
                              enum=get_regular_add_record_all_id()),
            openapi.Parameter('mood', openapi.IN_FORM, type=openapi.TYPE_STRING, description='心情'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # 用户打卡，该用户是否添加了这个打卡项，或者是否为该班级的打卡项，
        check = check_insert_info(request)
        if check:
            return check
        # 判断打卡的时间段

        resp = super().create(request)
        return response_success_200(data=resp.data)
