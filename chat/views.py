# chat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from .models import Group, Author, Message
from django.core.exceptions import ObjectDoesNotExist
from asgiref.sync import sync_to_async
from django.db import transaction
import asyncio
import json

@sync_to_async
def get_author(user):
    try:
        return Author.objects.get(user=user)
    except Author.DoesNotExist:
        raise ObjectDoesNotExist("Author does not exist for this user.")
    
@login_required
def chat(request, group_id):
    group = Group.objects.get(pk=group_id)
    messages = Message.objects.filter(group=group)

    context = {
        'group': group,
        'messages': messages,
    }
    return render(request, 'chat/chat.html', context)

@login_required
async def create_message(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content.strip():
            try:
                author = await get_author(request.user)
            except Author.DoesNotExist:
                return HttpResponse("Author does not exist for this user.", status=404)
            
            group_id = request.POST.get('group_id')
            group = get_object_or_404(Group, id=group_id)
            with transaction.atomic():
                message = Message.objects.create(author=author, group=group, content=content)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Message content cannot be empty.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

async def stream_chat_messages(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    async def event_stream():
        async for message in get_existing_messages(group):
            yield f"data: {json.dumps(message)}\n\n"
        last_id = await get_last_message_id(group)
        while True:
            new_messages = Message.objects.filter(id__gt=last_id, group=group).order_by('created_at').values(
                'author__user__username', 'content', 'created_at')
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1)

    async def get_existing_messages(group):
        messages = Message.objects.filter(group=group).order_by('created_at').values(
            'author__user__username', 'content', 'created_at')
        for message in messages:
            yield {
                'author__user__username': message['author__user__username'],
                'content': message['content'],
                'created_at': message['created_at'].isoformat(),
            }

    async def get_last_message_id(group):
        last_message = await Message.objects.filter(group=group).order_by('id').alast()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
