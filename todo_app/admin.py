from django.contrib import admin
from .models import *
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


# Register your models here.

#
admin.site.register(CustomUser)
admin.site.register(ToDoList)
admin.site.register(ToDoItem)