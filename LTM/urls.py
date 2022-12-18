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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import GAMES.views as gameviews
import Accounts.views as accountviews
app_name = "ltm"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', gameviews.home, name='home'),
    path('', gameviews.index, name='home'),
    path('games/', include('GAMES.urls')),
    path('accounts/', include('Accounts.urls')),
    path('channels/', include('Channels.urls')),
    path('notification/', gameviews.notification),
] + static("/media/", document_root="/home/copv/git/LTM/media/")

admin.site.site_header = "CYBORG Admin"
admin.site.site_title = "CTF"
admin.site.index_title = "CYBORG Admin Portal"
