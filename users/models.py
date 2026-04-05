from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from uuid import UUID
import uuid


# Create your models here.
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    short_note = models.CharField(max_length=200, null=True, blank=True)
    bio = models.CharField(null=True, blank=True,max_length=500)
    profile_img = models.ImageField(
        null=True,
        blank=True,
        upload_to="profiles/",
        default="profiles/user-default.png",
    )
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['-created']
        '''This is use to order the data according to the created object in the table and if we use "-created"  the data will show newest first'''

    @property
    def imageUrl(self):
        try:
            url = self.profile_img.url
        except:
            url = "/images/profiles/user-default.png"
        return url


class Skills(models.Model):
    owner = models.ForeignKey(
        Userprofile, null=True, on_delete=models.CASCADE, blank=True
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    Description = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Userprofile , null=True , on_delete=models.SET_NULL , blank=True)
    recipent = models.ForeignKey(Userprofile , null=True , on_delete=models.SET_NULL , blank=True , related_name="messages")
    name = models.CharField(max_length=200 , null=True , blank=True)
    email = models.EmailField(max_length=200 , null = True , blank=True)
    subject = models.CharField(max_length=200 , null=True , blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False , null= True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)



    def __str__(self):
        return self.subject
    




