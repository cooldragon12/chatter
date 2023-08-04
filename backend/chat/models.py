import uuid
from django.db import models
from account.models import User
# from django.utils.translation import ungettext_lazy as _
import random
import string
''' Models 
Consist:
    Room Model
    User Model
'''

def generate_secret_code(length=6):
    """ Generate Secret Code
        
        Generate random code from ascii in lower case.
    """
    while True:
        code = ''.join(random.choices(string.hexdigits, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code


# Create your models here
class Room(models.Model):
    """ Room Model
    
    Model of room to chat in and join in.
    """
    search_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    # Room Details
    name = models.CharField(max_length=100)
    max_users = models.IntegerField(blank=True)
    host = models.ForeignKey(User,on_delete=models.CASCADE, related_name="owner_of_room")
    # Not Editable
    code = models.CharField(unique=True, max_length=6, default=(generate_secret_code), editable=False)
    created_on =  models.DateTimeField(auto_now_add=True)
    # Room 
    members = models.ManyToManyField(User, blank=True, related_name="members_in_room")
    unique_code = models.CharField(max_length=15, default=generate_secret_code, editable=False)
    
    def __str__(self):
        return self.name
    def change_room_name(self, newName):
        self.name = newName
        self.save()
    def change_max_users(self, number):
        self.max_users= number
        self.save()
    @classmethod
    def get_total_members(self):
        return self.members.count()
    
""" Message Model

Model of message to send and receive.
"""
class Message(models.Model):
    encrypted_content = models.TextField()
    converation = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    status = models.CharField(max_length=10, default="sent", choices=[("sent", "sent"), ("received", "received"),("read", "read"), ("unread", "unread")])
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']

