import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *

from scraping.models import Vacancy, City, Language


from django.db import DatabaseError






parsers = (
    (work, 'https://www.work.ua/jobs-kyiv-python/'),
    (rabota, 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
    (djinni, 'https://djinni.co/jobs/keyword-python/kyiv/'),
)

city = City.objects.filter(slug='kiev')
language = Language.objects.filter(slug='python')

jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=Language)
    try:
        v.save()
    except DatabaseError:
        pass

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
