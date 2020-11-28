from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet

from examine.models import Examine
from examine.views.examine_serializers import ExamineInfoSerializersAll
from utils.my_info_judge import pd_token, lookup_token, STATUS_TOKEN_NO_AUTHORITY
from utils.my_response import response_success_200, response_error_400
from utils.my_utils import get_work_all_id, get_student_all_id


class ExamineInsertView(mixins.CreateModelMixin,
                        GenericViewSet):
    queryset = Examine.objects.all()
    serializer_class = ExamineInfoSerializersAll
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="学生提交作业",
        operation_description="说明：学生和作业必须存在，上传作业文件",
        manual_parameters=[
            openapi.Parameter('student', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='提交学生的id',
                              enum=get_student_all_id(), required=True),
            openapi.Parameter('work', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='作业的id',
                              enum=get_work_all_id(), required=True),
        ]
    )
    def create(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if lookup_token(request) is not 1:
            return response_error_400(status=STATUS_TOKEN_NO_AUTHORITY, message="不是学生提交什么作业？")
        print(request.data)
        resp = super().create(request)
        return response_success_200(data=resp.data)
