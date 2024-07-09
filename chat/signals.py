from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .utils import get_or_create_bible_study_group
from .models import Group

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    bible_study_group = get_or_create_bible_study_group()
    if not user.groups.filter(id=bible_study_group.id).exists():
        bible_study_group.members.add(user)

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    bible_study_group = get_or_create_bible_study_group()
    if not user.member_groups.filter(id=bible_study_group.id).exists():  # Make sure to use the correct related_name
        bible_study_group.members.add(user)