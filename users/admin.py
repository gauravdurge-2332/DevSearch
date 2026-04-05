from django.contrib import admin
from .models import Userprofile, Skills , Message

# Register your models here.
admin.site.register(Userprofile)
admin.site.register(Skills)
admin.site.register(Message)
