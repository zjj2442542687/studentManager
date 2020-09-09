from utils.my_response import response_error_400


def check_authority(self, request, kwargs):  # 检查权限问题
    # 需要修改的检测
    pk = kwargs['pk']
    if not self.queryset.filter(pk=pk):
        return response_error_400(message="id未找到")

    # 管理员的记录不能被别人删除，其他用户的只能自己删除
    regular_add_record_user = self.queryset.get(pk=pk).user
    regular_add_record_user_id = regular_add_record_user.id
    regular_add_record_user_role = regular_add_record_user.role
    if regular_add_record_user_id != request.user:  # 不是自己的
        if regular_add_record_user_role >= 0:  # 需要删除的regularAddRecord是普通用户的
            if request.auth >= 0:  # 执行的用户是普通用户
                return response_error_400(message="没有权限删除别人的东西!!!")
        else:  # 需要被删除的regularAddRecord是管理员的
            return response_error_400(message="不能删除管理员的东西!!!")


def check_info(request):  # 检查其它信息
    print(request.GET)

    pass
