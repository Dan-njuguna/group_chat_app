# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<int:group_id>/', views.chat, name='chat'),
    path('create-message/', views.create_message, name='create-message'),
    path('stream-chat-messages/', views.stream_chat_messages, name='stream_chat_messages'),
]