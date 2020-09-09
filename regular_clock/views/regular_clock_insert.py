from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular_add_record.models import RegularAddRecord
from regular_clock.models import RegularClock
from regular_clock.views.regular_clock_serializers import RegularClockInfoSerializersAll
from utils.my_info_judge import pd_super_adm_token, pd_token
from utils.my_response import response_success_200, response_error_400
from utils.my_swagger_auto_schema import request_body, string_schema
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
                              description='regular_add_record的id，你要给哪个打卡', required=True, enum=get_regular_add_record_all_id()),
            openapi.Parameter('mood', openapi.IN_FORM, type=openapi.TYPE_STRING, description='心情'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        regular_add_record_id = request.data.get("regular_add_record")
        if not regular_add_record_id:
            return response_error_400(message="regular_add_record不能为空")
        elif not RegularAddRecord.objects.filter(id=regular_add_record_id):
            return response_error_400(message="regular_add_record没找到该id")

        resp = super().create(request)
        return response_success_200(data=resp.data)
