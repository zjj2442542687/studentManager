from rest_framework.viewsets import ModelViewSet

from course.models import Course
from school.views.school_insert import SchoolInfoSerializers
from utils.my_info_judge import pd_token
from utils.my_response import response_success_200

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CourseOtherView(ModelViewSet):
    queryset = Course.objects.all()
    serializer_course = SchoolInfoSerializers

    @swagger_auto_schema(
        operation_summary="删除",
        pagination_class=None,
        manual_parameters=[
            openapi.Parameter('TOKEN', openapi.IN_HEADER, type=openapi.TYPE_STRING, description='管理员TOKEN'),
        ]
    )
    def destroy(self, request, *args, **kwargs):
        check_token = pd_token(request)
        if check_token:
            return check_token
        if request.auth >= 0:
            return response_success_200(message="没有权限")

        super().destroy(request, *args, **kwargs)
        return response_success_200(message="删除成功!!")
