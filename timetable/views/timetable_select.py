from timetable.models import Timetable
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from drf_yasg.utils import swagger_auto_schema

from timetable.views import views
from timetable.views.timetable_serializers import TimetableDepth2SerializersInsert
from utils.my_response import response_success_200
from utils.my_swagger_auto_schema import request_body, integer_schema


class TimetableSelectView(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableDepth2SerializersInsert

    @swagger_auto_schema(
        operation_summary="查询班级的课表",
        operation_description="传入班级id",
        request_body=request_body(properties={
            'class_id': integer_schema('班级id'),
        })
    )
    def select_class(self, request):
        class_id = request.data.get('class_id')
        print(class_id)

        timetable = self.queryset.filter(class_info_id=class_id)
        print(timetable)
        serializer = self.get_serializer(timetable, many=True)
        return response_success_200(data=serializer.data)
