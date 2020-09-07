from rest_framework.serializers import ModelSerializer

from regular_category.models import RegularCategory


class RegularCategoryInfoSerializersAll(ModelSerializer):
    class Meta:
        model = RegularCategory
        fields = "__all__"
