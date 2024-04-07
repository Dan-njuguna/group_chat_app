from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Room(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
