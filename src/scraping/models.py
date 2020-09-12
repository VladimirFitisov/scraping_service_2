from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Место вакансии', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)
    
    class Meta:
        verbose_name='Место ваканси'
        verbose_name_plural = 'Название населенных пунктов'
    
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык программирования', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирвания'

    def __str__(self):
        return self.name