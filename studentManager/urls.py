from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.views.generic import RedirectView
from studentManager import settings

schema_view = get_schema_view(
    openapi.Info(
        title="测试接口API",
        default_version='v1',
        description="接口文档",
        terms_of_service="#",
        contact=openapi.Contact(email="2639074625@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # drf-yasg 配置
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('parent/', include('parent.urls')),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls')),
    path('classs/', include('classs.urls')),
    path('timetable/', include('timetable.urls')),
    path('userDetails/', include('user_details.urls')),
    path('school/', include('school.urls')),
    path('course/', include('course.urls')),
    path('FileInfo/', include('FileInfo.urls')),
    path('', RedirectView.as_view(url='swagger')),
]

# 访问静态资源
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
