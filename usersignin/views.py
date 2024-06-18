from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm
from django.contrib.auth.models import User
from django.urls import reverse
from chat.models import Group

def signup(request):
    """
    Handles user signup process.

    Parameters:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: The rendered signup page if the request method is not POST or if form is invalid.
        HttpResponseRedirect: Redirects to the lobby page if the signup process is successful.
    """
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                # Handle case where username is already taken
                form.add_error('username', 'This username is already taken. Please choose a different one.')
                return render(request, 'usersignin/signup.html', {'form': form})
            
            # Create a new user with the form data
            user = User.objects.create_user(
                username=username,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['full_name'].split()[0],
                last_name=form.cleaned_data['full_name'].split()[1] if len(form.cleaned_data['full_name'].split()) > 1 else '',
                password=form.cleaned_data['password']
            )
            # Log the user in using authenticate and login functions
            authenticated_user = authenticate(request, username=username, password=form.cleaned_data['password'])
            login(request, authenticated_user, backend='django.contrib.auth.backends.ModelBackend')
            # Redirect to the lobby page
            return redirect('chat')
    else:
        # Create an empty signup form
        form = CustomSignupForm()
    
    # Render the signup page with the form
    return render(request, 'usersignin/signup.html', {'form': form})

def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handles user login process.

    Parameters:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: The rendered login page if the request method is not POST.
        HttpResponseRedirect: Redirects to the lobby page if the login process is successful.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the lobby page
                return redirect('chat')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    # Render the login page with the form
    return render(request, 'usersignin/login.html', {'form': form})

@login_required
def lobby(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        try:
            group = Group.objects.get(name=group_name)
            return redirect('chat', group_id=group.id)
        except Group.DoesNotExist:
            return render(request, 'lobby/lobby.html', {'error': 'No such group exists.'})
    return render(request, 'lobby/lobby.html')