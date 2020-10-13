"""
Отправка собщений https://docs.djangoproject.com/en/3.1/topics/email/
"""

import os, sys
import django

from django.contrib.auth import get_user_model


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"


django.setup()

from django.core.mail import EmailMultiAlternatives

subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'#текстовое письмо
html_content = '<p>This is an <strong>important</strong> message.</p>'# html-письмо
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.attach_alternative(html_content, "text/html")
msg.send()