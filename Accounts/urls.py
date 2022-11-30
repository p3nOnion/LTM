"""LTM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from Accounts.views import login_user, get_user, users, logout_request, register_request,profile

app_name = "accounts"
urlpatterns = [
    path('auth/login/', login_user, name='login'),
    path('users/<id>', get_user, name='get_user'),
    path('users/', users, name='get_all_user'),
    path('profile/', profile, name='profile'),
    path('auth/register/', register_request, name='register'),
    path('auth/logout/', logout_request, name='logout'),
]
