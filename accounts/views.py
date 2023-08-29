from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user, user.username, user.password)
            auth_login(request, user)
            return redirect('articles:index')

    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts_form.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # http://127.0.0.1:8000/accounts/login/?next=/articles/create/
            next_url = request.GET.get('next') # => /articles/create/

            return redirect(next_url or 'articles:index')
            # next 인자가 url에 있을 때 => '/articles/create/' or 'articles:index'
            # next 인자가 url에 없을 때 => None or 'articles:index'
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts_form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')