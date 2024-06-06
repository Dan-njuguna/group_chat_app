from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Message

@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    messages = room.messages.order_by('timestamp')
    return render(request, 'chat/room.html', {'room': room, 'messages': messages})