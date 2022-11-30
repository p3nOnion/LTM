from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth

import GAMES.forms
from .forms import NewUserForm
from Accounts.forms import EditUser
from django.shortcuts import redirect, render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from Accounts.models import Users
from django.core.exceptions import PermissionDenied
from GAMES.models import Game
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_auth(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect("home")
    return render(request=request, template_name="Accounts/login.html", context={"login_form": form})
def logout_request(request):
    logout_auth(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("accounts:login")
def get_user(request,id):
    if request.user.is_superuser or int(request.user.id) == int(id) :
        user = Users.objects.get(id=id)
        return render(request, template_name="Accounts/users.html", context={"users":user})
    else:
        return redirect("game:home")
def profile(request):
    if request.method=="POST":
        form= EditUser(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = Users.objects.filter(id=request.user.id)
            user.update(first_name=first_name,last_name=last_name,email=email)
            return redirect("accounts:profile")
    user = Users.objects.filter(id=request.user.id).first()
    if user == None:
        return redirect("accounts:login")
    games = Game.objects.filter(author=request.user.id)
    form = GAMES.forms.NewGameForm()
    user_f = EditUser()
    return render(request, template_name='Accounts/profile.html', context={"user":user,"games":games,"form":form,"user_f":user_f})

    pass
def users(request):
    if request.user.is_superuser:
        users= Users.objects.all()
        return render(request, template_name="Accounts/users.html", context={"users": users})
    else:
        return redirect("game:home")
def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = (form.cleaned_data.get('username'))
            email = (form.cleaned_data.get('email'))
            password = (form.cleaned_data.get('password1'))
            first_name=(form.cleaned_data.get('first_name'))
            last_name = (form.cleaned_data.get('last_name'))
            if Users.objects.filter(username=username).first() is None:
                user = Users(username=username,email=email,first_name=first_name,last_name=last_name)
                user.set_password(password)
                user.save()
                messages.info(request, u'The account "%s" has been successfully registered.' % email)
                return redirect("accounts:login")
            else:
                messages.error(request, u'User "%s" is already in use.' % username)
    else:
        form = NewUserForm()
    return render(request=request, template_name="Accounts/register.html", context={"register_form": form})

def delete_user(request,id):
    if request.user.is_superuser:
        user= Users.objects.get(id=id)
        user.delete()
        users = Users.objects.all()
        return render(request, template_name="Accounts/users.html", context={"users": users})
    else:
        raise PermissionDenied