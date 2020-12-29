from django.urls import path

from char import chat, consumers

websocket_urlpatterns = [
    path(r'ws/chat/<str:token>', chat.ChatConsumer),
    path(r'ws/notice/<str:token>', consumers.Consumer),
]
