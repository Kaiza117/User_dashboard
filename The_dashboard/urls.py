from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('login', views.login_page),
    path('register', views.register_page),
    path('users/register', views.register),
    path('users/login', views.login),
    path('dashboard/admin', views.dashboard),
    path('dashboard', views.dashboard),
    path('users/show/<int:id>', views.users_homepage),
    path('users/edit/<int:id>', views.edit),
    path('users/adminedit/<int:id>', views.adminedit),
    path('users/edit_users/<int:id>', views.edit_users),
    path('users/delete/<int:id>', views.delete),
    path('logout', views.logout),
    path('post/<int:id>', views.post)
]