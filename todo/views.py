from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


def todos(request):
    return render(request, 'todos.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(user)
                return render(request, 'todos.html')
            except IntegrityError:
                print("already exists")
                return render(request, 'signup.html',
                {'form': UserCreationForm(),
                'errors': "that username or password was already taken"})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm(), 'errors': "that username or password was alredy taken"})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/signup')
    else:
        return render(request, "todos.html")

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {"form": AuthenticationForm(), "errors": "username and password is incorrect"})
        else:
            login(request, user)
            return render(request, 'todos.html')
