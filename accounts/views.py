from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=user, password=password)
    if not user:
        messages.error(request, 'Invalid user or password!')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login successfully!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('index')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    val_password = request.POST.get('password2')

    if not name or not last_name or not email or not username or not password or not val_password:
        messages.error(request, 'Neither field can be empty.')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Invalid email.')
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, 'Password must be longer than 6 characters.')
        return render(request, 'accounts/register.html')

    if len(username) < 6:
        messages.error(request, 'Username must be longer than 6 characters.')
        return render(request, 'accounts/register.html')

    if password != val_password:
        messages.error(request, 'Password must be equals.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Successfully registered!')

    user = User.objects.create_user(username=username, email=email,
                                    password=password, first_name=name,
                                    last_name=last_name)
    user.save()

    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form':form})

    form = FormContact(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Error when submitting the form!')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form':form})

    description = request.POST.get('description')

    if len(description) < 5:
        messages.error(request, 'Description field must have more than five characters.')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form':form})

    form.save()
    messages.success(request, f"Contact {request.POST.get('name')} successfully saved!")
    return redirect('dashboard')


