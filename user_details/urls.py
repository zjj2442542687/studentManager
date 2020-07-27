from django.urls import path

from user.views.user_insert import UserInsertView
from user_details.views.user_details_insert import UserDetailsInsertView
from user_details.views.user_details_other import UserDetailsOtherView
from user_details.views.user_details_select import UserDetailsSelectView

urlpatterns = [
    # 添加一条数据
    path("insert", UserDetailsInsertView.as_view({'post': 'create'})),

    # 获得所有用户详情信息
    path("getAll", UserDetailsSelectView.as_view({'get': 'list'})),
    # 根据id获得用户详情信息
    # path("getUserDetailsById/<int:pk>", UserDetailsSelectView.as_view({'get': 'retrieve'})),
    # 根据用户id获得用户详情信息
    # path("getUserDetailsByUserId/<int:user_id>", UserDetailsSelectView.as_view({'get': 'retrieve_by_user_id'})),

    # 根据用户id修改用户详情信息
    path("update/<int:user_id>", UserDetailsOtherView.as_view({'patch': 'partial_update'})),

    # 根据用户id删除用户详情信息
    path("delete/<int:pk>", UserDetailsOtherView.as_view({'delete': 'destroy'})),
]
