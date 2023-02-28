from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.UserLogin, name='login'),
    path('', views.UserLogin, name='login'),
    path('register/', views.UserRegister, name='register'),
    path('logout', views.UserLogout, name='logout'),

    path('home/', views.home, name='home'),
    path('list/<int:pk>', views.ListTask, name='list'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('new-task/<int:pk>', views.CreateTask, name='create'),
    path('new-list/', views.createList, name='newlist'),
    path('delete-list/<int:pk>', views.deletelist, name='deletelist'),
]