"""Форма для ввода пользователя
    см. https://docs.djangoproject.com/en/3.1/topics/auth/default/#authenticating-users
"""

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model() # получение usera из базы данных

class UsersLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.Charfild(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Проверка пользователя существует ли он в системе, проверка на валидацию
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip() #получение
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exsits():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[0].password): #преобразовывает пароль из текста и проверяет с существующем в база данных
                raise forms.ValidationError('Пароль не верный')
            user = authenticate(email = email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(UsersLoginForm.self).clean(*args, **kwargs) #переопределение стандартной функции


