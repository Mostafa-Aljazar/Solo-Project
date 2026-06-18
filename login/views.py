from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/admin/')

    errors = {}
    form_data = {}

    if request.method == 'POST':
        form_data = request.POST
        errors = User.objects.login_validator(request.POST)

        if not errors:
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            user = authenticate(request, username=email, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('/admin/')
            else:
                errors['login'] = 'البريد الإلكتروني أو كلمة المرور غير صحيحة.'

    return render(request, 'login/login.html', {
        'errors': errors,
        'form_data': form_data,
    })


def logout_view(request):
    logout(request)
    return redirect('/login/')
