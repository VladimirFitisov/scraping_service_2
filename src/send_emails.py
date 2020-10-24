"""
Отправка собщений https://docs.djangoproject.com/en/3.1/topics/email/
"""

import os, sys
import django
import datetime

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from scraping_service.settings import EMAIL_HOST_USER

ADMIN_USER = EMAIL_HOST_USER

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

django.setup()
from scraping.models import Vacancy, Error

today = datetime.date.today()
subject = f"Рассылка вакансий {today}"
text_content = f"Рассылка вакансий {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет.</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')
users_dict = {}  # набор пользователя

for i in qs:
    users_dict.setdefault((i['city'], i['language']), [])
    users_dict[(i['city'], i['language'])].append(i['email'])
if users_dict:
    params = {'city_id__in': [], 'language_id__in': []}  # выбрать все значения  которые принадлежат этой паре
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)
    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]}</p>'
            html += f'<p>{row["company"]}</p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()
#Отправка письма с ошибками на почту админа
qs = Error.objects.filter(timestamp=today)
if qs.exists():
    error = qs.first()
    data = error.data
    _html = ''
    for i in data:
        _html += f'<p><a href="{i["url"]}">Error: {i["title"]}</a></p>'
    subject = f"Ошибки скрапинга {today}"
    text_content = "Ошибки скрапинга"
    to = ADMIN_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
