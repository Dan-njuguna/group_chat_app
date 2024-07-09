from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Group

def get_or_create_bible_study_group(user=None):
    try:
        group, created = Group.objects.get_or_create(
            name="Bible Study",
            defaults={'description': 'Default group for Bible Study', 'owner': user}
            )
        return group
    except IntegrityError:
        return Group.objects.get(name="Bible Study")

channel_layer = get_channel_layer()

def broadcast_message(group_id, message):
    async_to_sync(channel_layer.group_send)(
        f"chat_{group_id}",
        {
            'type': 'chat.message',
            'message': json.dumps(message),
        }
    )