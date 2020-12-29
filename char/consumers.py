
from channels.generic.websocket import JsonWebsocketConsumer

from char.models import UserNotice
from user.models import User
from utils.my_encryption import my_decode_token

coroutine_list = {}


class Consumer(JsonWebsocketConsumer):
    # 转换为key
    @staticmethod
    def id_to_key(user_id):
        return f'User{user_id}'

    @staticmethod
    def user_to_key(user):
        return f'User{user.id}'

    # 获取用户
    def to_user(self):
        print(self.scope.get('url_route').get('kwargs').get('token'))
        result = my_decode_token(self.scope.get('url_route').get('kwargs').get('token'))
        return User.objects.get(id=result[0] if len(result) > 0 else 0)

    # 连接
    def connect(self):
        user = self.to_user()
        if user and isinstance(user, User):
            key = Consumer.id_to_key(user)
            if key in coroutine_list:
                coroutine_list[key].append(self)
            else:
                coroutine_list[key] = [self]
            self.accept()
            # 发送未读通知
            UserNoticeSend.send_user_all_unread_notice(user, self)

    # 断开
    def disconnect(self, close_code):
        user = self.to_user()
        if user:
            key = Consumer.id_to_key(user)
            if key in coroutine_list:
                coroutine_list[key].remove(self)

    @staticmethod
    def send_to_user(user, json):
        is_send = False
        key = Consumer.id_to_key(user)
        if key in coroutine_list:
            for coroutine in coroutine_list[key]:
                coroutine.send_json(json)
                if not is_send:
                    is_send = True
        return is_send

    # 收到信息
    def receive_json(self, content, **kwargs):
        user = self.to_user()
        if isinstance(user, User):
            genre: int = content.get('type', 'message')
            # 获取历史通知
            if genre == 'history':
                notice_list = UserNotice.objects.all()
                # 信息类型
                level: int = content.get('level')
                page: int = content.get('page', 1)
                size: int = content.get('size', 5)
                if level:
                    notice_list = notice_list.filter(level=level)
                notice_list = notice_list.filter(user=user)[(page - 1) * size:page * size]
                if notice_list:
                    for notice in notice_list:
                        pass
                        # self.send_to_user(user, UserNoticeSerializer(notice).data)
                else:
                    self.send_to_user(user, {'id': -1})
            # 删除通知
            elif genre == 'delete':
                message_id = content.get('id', 0)
                UserNotice.objects.filter(user=user, pk=message_id).delete()


# --------------------------------------------------用户通知--------------------------------------------------
class UserNoticeSend:
    @staticmethod
    # 发送通知给用户 coroutine为None时发送所有该用户在线用户 coroutine不为空时发送给coroutine
    def send_user_notice(user, notice: UserNotice, coroutine=None):
        if coroutine:
            # 发送一个用户
            print(notice.to_json())
            coroutine.send_json(notice.to_json())
            is_send = True
        else:
            # 发送当前连接的所有账号
            is_send = Consumer.send_to_user(user, notice.to_json())
        if is_send:
            notice.status = 1
            notice.save()

    # 发送未读消息给用户
    @staticmethod
    def send_user_all_unread_notice(user: User, coroutine=None):
        unread_notice = UserNotice.objects.filter(user=user, status=0).order_by('id')
        for notice in unread_notice:
            UserNoticeSend.send_user_notice(user, notice, coroutine=coroutine)

    # 发送通知给用户
    @staticmethod
    def send_notice(notice_user: User, level: int, _id: int):
        if level == 0:
            notice = UserNotice.objects.create(user=notice_user, level=level, work_id=_id)
            # 发送当前在线用户
            UserNoticeSend.send_user_notice(notice_user, notice)
        elif level == 1:
            notice = UserNotice.objects.create(user=notice_user, level=level, examine_id=_id)
            # 发送当前在线用户
            UserNoticeSend.send_user_notice(notice_user, notice)
