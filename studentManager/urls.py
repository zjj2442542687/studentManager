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
    path('', RedirectView.as_view(url='swagger')),

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
    # 周
    path('week/', include('week.urls')),
    # 习惯养成类别
    path('regularCategory/', include('regular_category.urls')),
    # 习惯养成
    path('regular/', include('regular.urls')),
    # 习惯养成用户的添加
    path('regularAddRecord/', include('regular_add_record.urls')),
    # 习惯养成用户的打卡
    path('regularClock/', include('regular_clock.urls')),
    # 作业发布
    path('work/', include('work.urls')),
    # 作业审核
    path('examine/', include('examine.urls')),
    # 学校管理员
    path('schooladm/', include('schooladm.urls')),
    path('FileInfo/', include('FileInfo.urls')),
]

# 访问静态资源
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
