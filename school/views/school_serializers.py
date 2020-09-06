from rest_framework.serializers import ModelSerializer

from school.models import School


class SchoolSerializersSearch(ModelSerializer):
    # 查询
    class Meta:
        model = School
        fields = ["id", "school_name", "school_info", "school_date"]
