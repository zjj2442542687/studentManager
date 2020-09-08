from rest_framework.serializers import ModelSerializer

from week.models import Week


class WeekInfoSerializersAll(ModelSerializer):
    class Meta:
        model = Week
        fields = "__all__"
