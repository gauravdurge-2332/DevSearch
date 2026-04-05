from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db import IntegrityError
from .models import Userprofile
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Userprofile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

       
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER ,
        #     [profile.email],
        #     fail_silently=False,

        # )



@receiver(post_delete, sender=Userprofile)
def deleteuser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


@receiver(post_save, sender=Userprofile)
def updateuser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        try:
            user.save()
        except IntegrityError:
            pass # Gracefully handle duplicate username/email errors without crashing
