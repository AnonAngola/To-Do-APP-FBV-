from django.forms import ModelForm
from .models import ToDoItem, ToDoList, CustomUser

class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','password']

class todoitemForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = '__all__'

class todolistForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title']