
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.serializers import ModelSerializer

from user_details.models import UserDetails
from utils.my_response import response_success_200


class UserDetailsInfoSerializers(ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ["user"]


class UserDetailsInsertView(mixins.CreateModelMixin,
                            GenericViewSet):
    """
    create:
    添加一条数据

    无描述
    """
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsInfoSerializers

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return response_success_200(data=resp.data)

