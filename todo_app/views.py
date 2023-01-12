from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .form import CustomUserForm, todoitemForm, todolistForm
from .models import *

# AUTHENTICATION

def UserLogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'GET':
            Is_login = True
            context = {'form':CustomUserForm, 'Is_login':Is_login}
            return render(request, 'login.html', context)
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('  Credenciais inválias')

def UserRegister(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        Username = request.POST.get('Username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        user = CustomUser.objects.create_user(password=password, email=email, Username=Username)

        if len(Username.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0 or password != password2:
            return render('register')
        else:
            user.save()
            return redirect('login')

def UserLogout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
        use = request.user
        todo_list = ToDoList.objects.filter(userID_id=use.id)
        context = {'todo_list':todo_list,}
        return render(request, 'home.html', context)

@login_required
def list(request, pk):
    items = ToDoItem.objects.filter(todo_list_id=pk)
    list_title = get_object_or_404(ToDoList,pk=pk)
    context = {'items':items, 'list_title':list_title}
    return render(request, 'list.html', context)

@login_required
def update(request, pk):

    if request.method == 'GET':
        item = ToDoItem.objects.get(pk=pk)
        list_id = ToDoItem.objects.get(pk=pk).todo_list_id
        actual_list = ToDoList.objects.get(pk=list_id)
        form = todoitemForm(request.POST or None, instance=item)
        context = {'item':item, 'form':form, 'actual_list':actual_list}
        return render(request, 'update.html', context)

    else:
        item = ToDoItem.objects.get(pk=pk)
        list_id = ToDoItem.objects.get(pk=pk).todo_list_id
        form = todoitemForm(request.POST or None, instance=item)
        context = {'form':form}

        if form.is_valid():
            obj= form.save(commit= False)
            obj.save()
            return redirect('list', pk=list_id)
        else:
            context= {'form': form,
                        'error': 'The form was not updated successfully. Please enter in a title and content'}
            return render(request,'update.html' , context)

@login_required
def delete(request, pk):
    list_id = get_object_or_404(ToDoItem,pk=pk).todo_list_id
    item = ToDoItem.objects.get(pk=pk)
    item.delete()
    return redirect('list', pk=list_id)

@login_required
def create(request, pk):
    if request.method == 'GET':
        actual_list = ToDoList.objects.get(pk=pk)
        form = todolistForm(request.POST or None)
        context = {'form':form, 'actual_list':actual_list}
        return render(request, 'create.html', context)
    else:
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        todo_list = request.POST['todo_list']
        form = ToDoItem(title=title, description=description, due_date=due_date, todo_list_id=todo_list)
        form.save()
        return redirect('list', pk=pk)

@login_required
def createList(request):
    user = request.user
    if request.method == 'GET':
        form = todolistForm(request.POST or None)
        return render(request, 'createList.html', {'form':form,'user':user})
    else:
        title = request.POST.get('title')
        userID = user.id
        form = ToDoList(title=title, userID_id=userID)
        form.save()
        return redirect('index')

@login_required
def deletelist(request, pk):
    list = ToDoList.objects.get(pk=pk)
    list.delete()
    return redirect('index')
