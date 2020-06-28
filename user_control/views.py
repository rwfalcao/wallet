from django.shortcuts import render
from user_control.forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def sign_up(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            username = signup_form.cleaned_data.get('email')
            raw_password = signup_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
            # return render(request, 'index.html')

    else:
        signup_form = SignUpForm()
        login_form = LoginForm()
    return render(request, 'sign_up.html', {
        'signup_form': signup_form,
        'login_form': login_form,
        })


def user_logout(request):
    logout(request)
    return redirect('/user_auth/')


def user_authenticate(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = authenticate(
            username=login_form.cleaned_data['email'], 
            password=login_form.cleaned_data['password']
            )
    login(request, user)
    return redirect('/')






