from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError


def todos(request):
    return render(request, 'todos.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return render(request, 'todos.html')
            except IntegrityError:
                print("already exists")
                return render(request, 'signup.html',
                {'form': UserCreationForm(),
                'errors': "that username or password was already taken"})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm(), 'errors': "that username or password was alredy taken"})
