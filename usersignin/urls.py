# usersignin/urls.py

from django.urls import path
from . import views as usersignin_views

urlpatterns = [
    path('lobby/', usersignin_views.lobby, name='lobby'),
    path('signup/', usersignin_views.signup, name='signup'),
    path('', usersignin_views.login_view, name='login'),
    #path('logout/', usersignin_views.logout_view, name='logout'),
]