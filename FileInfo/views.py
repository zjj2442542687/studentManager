from django.http import FileResponse

# Create your views here.
from django.utils.http import urlquote
from rest_framework import mixins
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet
from utils.my_response import *
from FileInfo.models import FileInfo


class FileInfoSerializer(ModelSerializer):
    class Meta:
        model = FileInfo
        fields = '__all__'


class FileInfoView(RetrieveModelMixin, CreateModelMixin, GenericViewSet, ListModelMixin, DestroyModelMixin):
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer
    parser_classes = [MultiPartParser]


class FileInfoDownloadView(mixins.CreateModelMixin,
                           GenericViewSet):
    """
    download:
    文件下载

    无描述
    """
    queryset = FileInfo.objects.all()
    serializer_class = FileInfoSerializer

    def download(self, request, *args, **kwargs):
        file_info = FileInfo.objects.get(id=kwargs.get('pk'))
        # print(file_info)
        # print('下载的文件名：' + file_info.file_name)
        # print(file_info.file)
        file = open(file_info.file.path, 'rb')
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment;filename="%s"' % urlquote(file_info.file_name)
        return response
