""" Функция входа и выхода
https://docs.djangoproject.com/en/3.1/topics/auth/default/
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from accounts.forms import UserLoginForm

#функция входа
def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        #получение данных из формы
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        #аутентификация usera
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')#после успешного заполнения формы, перенаправляем на главную страницу
    return render(request, 'accounts/login.html', {'form': form}) #если форма не заполнена мы должны вернуть рендер и загрузить страничку с регистрацией
# + создать файл accounts/urls для подключения данных вюшек
#функция выхода

def logout_view(request):
    logout(request)
    return redirect('home')