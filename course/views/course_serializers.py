from rest_framework.serializers import ModelSerializer

from course.models import Course


class CourseALlSerializers(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
