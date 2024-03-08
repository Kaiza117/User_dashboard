from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    # For user level, admin is 1 and non-admin is 2.
    user_level = models.IntegerField(default = 2)
    description = models.TextField(default='description')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Message(models.Model):
    message = models.TextField()
    message_author = models.ForeignKey(User, related_name = 'messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    profile = models.IntegerField(default = 1)

class Comment(models.Model):
    comment = models.TextField()
    comment_author = models.ForeignKey(User, related_name = 'comments',on_delete=models.CASCADE)
    comment_message = models.ForeignKey(Message, related_name = 'comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
