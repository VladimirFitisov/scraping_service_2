import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language

parsers = ((work, 'https://www.work.ua/jobs-python/'),
           (rabota, 'https://rabota.ua/zapros/python/%d1%83%d0%ba%d1%80%d0%b0%d0%b8%d0%bd%d0%b0'),
           (dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
           (djinni, 'https://djinni.co/jobs/keyword-python/')
           )
city = City.objects.filter(slug='kiev')
jobs, errors = [], []

for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()