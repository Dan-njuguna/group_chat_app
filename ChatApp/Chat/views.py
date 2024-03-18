from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def get(self, request):
        return render(request, 'loginPage.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('chatpage'))
        else:
            return Response({"error": "Invalid login credentials"}, status=status.HTTP_400_BAD_REQUEST)

    def chatpage(self, request):
        if request.user.is_authenticated:
            return render(request, 'templates/chatPage.html')
        else:
            return HttpResponseRedirect(reverse('login'))
