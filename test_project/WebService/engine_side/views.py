from asgiref.sync import sync_to_async
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .tokening import create_token
from .models import User, Table, Message



@csrf_protect
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'login.html')
    else:
        form = UserCreationForm()
    return render(request, 'reg.html', {'form': form})

@csrf_protect
def login_user(request):
    user = None   
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('test')
        else:
            messages.error(request, 'Invalid username or password')
    if user is not None:
        messages.success(request, 'Logged in successfully')
    else:
        messages.info(request, 'Please enter your credentials and submit')

    return render(request, 'login.html')

def logout_user(request):
	logout(request)
	messages.success(request, ("U have successfully logged out"))
	return redirect('info')

def contact_view(request):
    context = {
        'telegram_link': 'https://telegram.me/LesMoustache'
    }
    return render(request, 'info.html', context)

@ensure_csrf_cookie
@login_required
def test(request):
	token = create_token(user_id=request.user.id)
	return render(request, 'test.html', {'token':token})
