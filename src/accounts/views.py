""" Функция входа и выхода
https://docs.djangoproject.com/en/3.1/topics/auth/default/
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib import messages  # для вывода сообщений https://docs.djangoproject.com/en/3.1/ref/contrib/messages/

from accounts.forms import UserLoginForm, UserRegistrationform, UserUpdateForm, ContactForm
from scraping.models import Error

import datetime as dt

User = get_user_model()


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
        messages.success(request, 'Пользователь добавлен в систему')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})


# форма кабинета пользователя, которая позволяет проверить какие у него настройки
def update_view(request):
    contact_form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Данные сохранены')
                return redirect('accounts:update')

        form = UserUpdateForm(
            initial={'city': user.city, 'language': user.language, 'send_email': user.send_email}
        )
        return render(request, 'accounts/update.html', {'form': form, 'contact_form': contact_form})
    else:
        return redirect('accounts:login')


# Удаление пользователя
def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удален :(')
    return redirect('home')


# функция добавления сообщения от пользователей
def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())  # получение записи из бд, есть ли ошибки
            if qs.exist():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'language': language, 'email': email})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'language': language, 'email': email}]
                Error(data=f"user_data: {data}").save()
            messages.success(request, 'Данные отправлены администрации')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
