from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.utils import timezone

##### USER #####


def signupuser(request):
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


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/login')
    else:
        return render(request, "todos.html")


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {"form": AuthenticationForm(), "errors": "username and password is incorrect"})
        else:
            login(request, user)
            return redirect('/')


##### Todos #####
def todos(request):
    user = request.user
    try:
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
        print(f'*** user = {user} ***')
        return render(request, 'todos.html', {'todos': todos})
    except:
        print(f"couldn't handle it")
        return render(request, 'todos.html')
    # todos = Todo.objects.all()



def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('/')
        except ValueError:
            return render(request, 'createtodo.html', {'form': TodoForm(), 'errors': "bad data passed in"})

def updatetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'updatetodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('/')
        except ValueError:
            return render(request, 'updatetodo.html', {'todo': todo, 'form': form, 'error': "bad info"})

def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('/')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('/')

def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, 'todos.html', {'todos': todos})