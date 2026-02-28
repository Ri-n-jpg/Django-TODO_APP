from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import TODOO

# Home redirects to todo page
@login_required(login_url='/login/')
def home(request):
    return redirect('/todopage/')

# Signup view
def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        User.objects.create_user(fnm, emailid, pwd)
        return redirect('/login/')
    return render(request, 'signup.html')

# Login view
def user_login(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        user = authenticate(request, username=fnm, password=pwd)
        if user:
            auth_login(request, user)
            return redirect('/todopage/')
        else:
            return redirect('/login/')
    return render(request, 'login.html')

# Todo page with inline add/edit
@login_required(login_url='/login/')
def todo(request):
    # Add new todo
    if request.method == 'POST' and 'add_todo' in request.POST:
        title = request.POST.get('title')
        if title.strip():  # prevent empty todos
            TODOO.objects.create(title=title, user=request.user)
        return redirect('/todopage/')

    # Edit todo inline
    if request.method == 'POST' and 'edit_todo' in request.POST:
        srno = request.POST.get('srno')
        todo_obj = TODOO.objects.get(srno=srno, user=request.user)
        todo_obj.title = request.POST.get('title')
        todo_obj.save()
        return redirect('/todopage/')

    todos = TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': todos})

# Delete todo
@login_required(login_url='/login/')
def delete_todo(request, srno):
    TODOO.objects.filter(srno=srno, user=request.user).delete()
    return redirect('/todopage/')

# Logout view
@login_required(login_url='/login/')
def signout(request):
    auth_logout(request)
    return redirect('/login/')