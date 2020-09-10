from rest_framework import serializers

from regular_category.models import RegularCategory


class RegularCategoryInfoSerializersAll(serializers.ModelSerializer):
    class Meta:
        model = RegularCategory
        fields = "__all__"


class RegularCategorySerializersSearch(serializers.ModelSerializer):

    class Meta:
        model = RegularCategory
        fields = "__all__"

