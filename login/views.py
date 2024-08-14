from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'login/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = name
            user.save()
            return redirect('login')
        
    return render(request, 'login/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            name = user.first_name
            name = name.capitalize()
            return render(request, 'login/dashboard.html', {'name': name})
        else:
            #messages.error('Not Found')
            return redirect('register')

    return render(request, 'login/login_page.html')

def logout(request):
    auth_logout(request)
    return redirect('')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'login/dashboard.html')

def change_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']

        user = authenticate(request, username=username, password=old_password)

        if user is not None:
            user.set_password(new_password)
            user.save()
            return redirect('login')
        else:
            return redirect('')

    return render(request, 'login/change-password.html')