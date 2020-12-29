from django.urls import path

from char import chat

websocket_urlpatterns = [
    path(r'ws/chat/<str:token>', chat.ChatConsumer),
]
