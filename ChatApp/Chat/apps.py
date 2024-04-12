from django.apps import AppConfig
from django.shortcuts import render
from django.http import HttpResponse

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chat'

# def dan_ni_mbwa(request):
#     return render(request, 'Chat/dan_ni_mbwa.html')

# def login_page(request):
#     return render(request, 'Chat/loginPage.html')