from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    
    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username})

# Import the messages model
from .models import Message

# Get the messages from the database
messages = Message.objects.filter(room=room_name)[0:25]

# Add the messages to the context
'messages': messages
