from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (User,
                     Room,
                     Message)
# from .form import Form

# def chatpage(request, *args, **kwargs):
#     if not request.user.is_authenticated:
#         return redirect("login-user")
#     context = {}
#     return render(request,"Chat/templates/chatPage.html", context)

class LoginView(APIView):
    '''
    This class is made to render the login page.
    Functions:
        1. get(self, request): renders the login form to the user.
        2. post(self, request): Posts data collected on the Form to the database and validates if the user if valid or not.
        3. chatpage(self, request): renders the chatpage if the user is authenticated.
    '''
    
    def get(self, request):
        '''
        This function renders the login form to the user.
        @login: The login query variable saving data from the sqlite database.
        @cont: the login data saved as a dictionary. To work as JSON.
        '''
        login = User.objects.all()
        cont = {
            "login": login,
        }
        return render(request, 'templates/loginPage.html', cont)
    
    # @csrf_exempt
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
