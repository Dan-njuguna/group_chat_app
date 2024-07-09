# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:group_id>/', views.chat, name='chat'),
    path('create_message/', views.create_message, name='create_message'),
    path('chat/stream-chat-messages/<int:group_id>/', views.stream_chat_messages, name='stream_chat_messages'),
]