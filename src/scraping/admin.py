from django.contrib import admin
from .models import *

# Регистрация моделей в админке
admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
