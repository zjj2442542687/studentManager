from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import Q

from char.models import UserCharRecord
from user.models import User
from utils.my_encryption import my_decode_token

chat_list = {}


class ChatConsumer(JsonWebsocketConsumer):
    # 连接方式
    # ws://127.0.0.1:8000/ws/chat/MSAxIGNYRnhjUSAxNjA5MjM2NzE3LjA5ODMwOQ

    # 发送JSON
    # {
    #
    #     "type": "chat",
    #     "receive": 2,
    #     "content": "你爸爸"
    # }
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

    def connect(self):
        # 获取用户
        user = self.to_user()
        # 判断是否获取用户
        if user and isinstance(user, User):
            print(f'{user}连接')
            # 获取用户对应key值
            key = ChatConsumer.user_to_key(user)
            if key in chat_list:
                chat_list[key].append(self)
            else:
                chat_list[key] = [self]
            self.accept()
            # 发送未读信息给用户
            self.send_user_all_unread_message(user)

    def disconnect(self, close_code):
        user = self.to_user()
        if user:
            print(f'{user}断开')
            key = ChatConsumer.user_to_key(user)
            if key in chat_list:
                chat_list[key].remove(self)

    def receive_json(self, content, **kwargs):
        print(content)
        send_user: User = self.to_user()
        # 获取消息类型
        genre: int = content.get('type', 'chat')
        # 发送消息
        if genre == 'chat':
            # 获取发送和接收方
            receive = content.get('receive')
            try:
                receive_user: User = User.objects.get(pk=receive)
            except User.DoesNotExist:
                return
            content['send'] = send_id = send_user.id
            # 获取发送内容
            send_content = content.get('content')
            # 写入数据库
            try:
                message = UserCharRecord.objects.create(send_id=send_id, receive=receive_user, content=send_content)
                ChatConsumer.send_message(message)
            except Exception:
                pass
            # 获取历史消息
        elif genre == 'history':
            page: int = content.get('page', 1)
            size: int = content.get('size', 5)
            message_list = UserCharRecord.objects.filter(Q(send=send_user) | Q(receive=send_user))[
                           (page - 1) * size:page * size]
            if message_list:
                for message in message_list:
                    self.send_message1(message)
            else:
                self.send_json({'id': -1})

    @staticmethod
    def send_message(message: UserCharRecord):
        # 发送发送方
        send_key = ChatConsumer.id_to_key(message.send.id)
        if send_key in chat_list:
            for coroutine in chat_list[send_key]:
                coroutine.send_message1(message)
        # 发送接收方
        receive_key = ChatConsumer.id_to_key(message.receive.id)
        is_send = False
        if receive_key in chat_list:
            for coroutine in chat_list[receive_key]:
                coroutine.send_message1(message)
                if not is_send:
                    is_send = True
        # 判断接收方是否收到消息
        if is_send:
            message.status = 1
            message.save()

    def send_message1(self, message: UserCharRecord):
        self.send_message2(message.id, message.send.id, message.receive.id, message.content, str(message.create_time))

    def send_message2(self, _id: int, send: int, receive: int, content: str, time):
        self.send_json(
            {
                'id': _id,
                'send': send,
                'receive': receive,
                'content': content,
                'time': time
            }
        )

    #  发送未读消息给用户
    def send_user_all_unread_message(self, user: User):
        unread_message = UserCharRecord.objects.filter(send=user, status=0).order_by('id')
        for message in unread_message:
            self.send_message1(message)
            message.status = 1
            message.save()
