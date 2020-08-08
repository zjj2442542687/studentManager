from rest_framework.viewsets import ModelViewSet, GenericViewSet
from classs.models import Class
from classs.views.class_select import ClassInfoSerializers2


class ClassOtherView(ModelViewSet):
    """
    destroy:
    根据id删除班级信息

    输入班级id删除

    """
    queryset = Class.objects.all()
    serializer_class = ClassInfoSerializers2

    def destroy(self, request, *args, **kwargs):
        # print("11111")
        return super().destroy(request, *args, **kwargs)
