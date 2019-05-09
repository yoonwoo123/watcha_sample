from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def list(request):
    users = get_user_model().objects.all()
    context = {'users': users}
    return render(request, 'accounts/list.html', context)
    
def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('accounts:list')
    else:
        user_form = UserForm()
        context = {'user_form': user_form}
        return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect('accounts:list')
    else:
        login_form = AuthenticationForm(request)
        context = {'login_form': login_form}
        return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:list')

@login_required
def follow(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.user in user.follwers.all():
        user.follwers.remove(request.user)
    else:
        user.follwers.add(request.user)
    return redirect('accounts:list')