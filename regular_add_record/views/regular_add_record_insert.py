from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from regular.models import Regular
from regular.views.regular_serializers import RegularInfoSerializersAll
from regular.views.views import check_insert_info
from regular_add_record.models import RegularAddRecord
from regular_add_record.views.regular_add_record_serializers import RegularAddRecordInfoSerializersAll
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200, response_error_400


class RegularAddRecordInsertView(mixins.CreateModelMixin,
                                 GenericViewSet):
    queryset = RegularAddRecord.objects.all()
    serializer_class = RegularAddRecordInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="添加数据 ",
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='用户的token'),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token

        # title = request.data.get("title")
        # regular_category_id = request.data.get("regular_category")
        # user_id = request.data.get("user")
        #
        # check = check_insert_info(title, regular_category_id, user_id)
        # if check:
        #     return check

        resp = super().create(request)
        return response_success_200(data=resp.data)
