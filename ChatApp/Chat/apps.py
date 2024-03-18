from django.apps import AppConfig
from django.shortcuts import render
from django.http import HttpResponse

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chat'
