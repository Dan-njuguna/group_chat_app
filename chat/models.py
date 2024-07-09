# models.py

from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='member_groups')

    def __str__(self):
        return self.name

class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='messages')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.user.username} - {self.content}'