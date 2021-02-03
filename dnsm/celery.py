# -*- encoding: utf-8 -*-
# File    : celery.py.py
# Time    : 2020/11/6 4:31 下午
# Author  : ops

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

app = Celery('dnsm')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')
