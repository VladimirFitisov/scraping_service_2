"""Форма для ввода пользователя
    см. https://docs.djangoproject.com/en/3.1/topics/auth/default/#authenticating-users
"""

from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping.models import City, Language

User = get_user_model()  # получение usera из базы данных


# Форма для входа пользователя
class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Проверка пользователя существует ли он в системе, проверка на валидацию
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, qs[
                0].password):  # преобразовывает пароль из текста и проверяет с существующем в база данных
                raise forms.ValidationError('Пароль не верный')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключен')
        return super(UserLoginForm, self).clean(*args, **kwargs)  # переопределение стандартной функции


# Форма для регистрации нового пользователя
class UserRegistrationform(forms.ModelForm):
    email = forms.CharField(label='Введите email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta():
        model = User  # создаем форму на основе модели User
        fields = ('email',)

        def clean_password2(self):
            data = self.cleaned_data
            if data['password'] != data['password2']:
                raise forms.ValidationError('Пароли не совпадают')
            return data['password2']


# форма для обновления данных пользователя
class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(), to_field_name="slug", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Cпециальность'
    )
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,
                                    label='Получать рассылку?')

    class Meta():
        model = User  # создаем форму на основе модели User
        fields = ('email', 'language', 'send_email')