# chat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from .models import Group, Author, Message
from django.db.models import Max
from django.db.models.functions import Coalesce
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
@require_POST
def create_message(request):
    content = request.POST.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Message content cannot be empty.'}, status=400)
    
    group_id = request.POST.get('group_id')
    group = get_object_or_404(Group, id=group_id)
    
    try:
        with transaction.atomic():
            message = Message.objects.create(author=request.user, group=group, content=content)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': True, 'message': {
        'author__name': message.author.username,
        'content': message.content,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }})

async def stream_chat_messages(request, group_id):
    async def get_group_or_404(group_id):
        return await sync_to_async(get_object_or_404)(Group, id=group_id)

    async def get_existing_messages(group):
        messages = await sync_to_async(list)(Message.objects.filter(group=group).order_by('created_at').values(
            'author__user__username', 'content', 'created_at'
        ))
        for message in messages:
            yield {
                'author__user__username': message['author__user__username'],
                'content': message['content'],
                'created_at': message['created_at'].isoformat(),
            }

    async def get_last_message_id(group):
        last_message = await sync_to_async(Message.objects.filter(group=group).aggregate)(
            last_id=Coalesce(Max('id'), 0)
        )
        return last_message['last_id']

    async def get_new_messages(last_id, group):
        new_messages = await sync_to_async(list)(
            Message.objects.filter(id__gt=last_id, group=group).order_by('created_at').values(
                'author__user__username', 'content', 'created_at', 'id'
            )
        )
        return new_messages

    group = await get_group_or_404(group_id)

    async def event_stream():
        async for message in get_existing_messages(group):
            yield f"data: {json.dumps(message)}\n\n"
        last_id = await get_last_message_id(group)
        while True:
            new_messages = await get_new_messages(last_id, group)
            for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1)

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'

    return response
