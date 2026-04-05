from django.contrib import admin
from .models import *

# Register your models here.

# class Projects(admin.ModelAdmin):
#     list_display = ('title','description',
#     'demo_link' ,
#     'source_link',
#     'tags' ,
#     'vote_total',
#     'created',
#     'id' ,
#     )
admin.site.register(Tags)
admin.site.register(Review)
admin.site.register(Project)
