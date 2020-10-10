""" Функция входа и выхода
https://docs.djangoproject.com/en/3.1/topics/auth/default/
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm, UserRegistrationform, UserUpdateForm


# функция входа
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        # получение данных из формы
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        # аутентификация usera
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')  # после успешного заполнения формы, перенаправляем на главную страницу
    return render(request, 'accounts/login.html', {
        'form': form})  # если форма не заполнена мы должны вернуть рендер и загрузить страничку с регистрацией


# + создать файл accounts/urls для подключения данных вюшек
# функция выхода

def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationform(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


# форма, которая позволяет проверить какие у него настройки
def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm()
        else:
            form = UserUpdateForm(
                initial={'city': user.city, 'language': user.language, 'send_email': user.send_email}
            )
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('accounts:login')