from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from schooladm.models import Schooladm


class SchooladmSerializer(ModelSerializer):
    class Meta:
        model = Schooladm
        fields = '__all__'


class SchooladmView(RetrieveModelMixin, CreateModelMixin, GenericViewSet, ListModelMixin, DestroyModelMixin):
    queryset = Schooladm.objects.all()
    serializer_class = SchooladmSerializer
    parser_classes = [MultiPartParser]