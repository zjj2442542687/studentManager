from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.generics import get_object_or_404

from student.models import Student
from student.views.student_serializers import StudentInfoSerializersUpdate
from utils.my_response import response_success_200, response_error_400
from utils.status import STATUS_TOKEN_OVER, STATUS_PARAMETER_ERROR


class StudentOtherView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentInfoSerializersUpdate
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="修改",
        required=[],
        manual_parameters=[
            openapi.Parameter('sex', openapi.IN_FORM, type=openapi.TYPE_INTEGER,
                              description='性别((-1, 女), (0, 保密), (1, 男))'),
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='TOKEN')
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        if request.user == STATUS_TOKEN_OVER:
            return response_error_400(staus=STATUS_TOKEN_OVER, message="token失效")
        elif request.user == STATUS_PARAMETER_ERROR:
            return response_error_400(staus=STATUS_PARAMETER_ERROR, message="token参数错误!!!!!")

        resp = super().partial_update(request, *args, **kwargs)
        return response_success_200(data=resp.data)

    def get_object(self):
        if self.action == "partial_update":
            print(self.request.user)
            # return self.queryset.get(user=user_id)
            return get_object_or_404(self.queryset, user_info_id=self.request.user)
        return super().get_object()
