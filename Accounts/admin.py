from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Accounts.forms import CustomUserChangeForm,CustomUserCreationForm
from Accounts.models import Users
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Users
    list_display = ['username', 'email', 'score','is_staff']

admin.site.register(Users, CustomUserAdmin)