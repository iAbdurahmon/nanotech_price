from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('category_list')
        else:
            messages.success(request, ("You are not allowed to login! Contact admin!"))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_user(request):
    logout(request)
    return redirect('login')
