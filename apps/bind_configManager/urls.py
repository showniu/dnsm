# -*- encoding: utf-8 -*-
# File    : urls.py.py
# Time    : 2020/10/12 11:22 上午
# Author  : ops
from django.conf.urls import url
from .views import BindConfigGenerateOps
from .views import BindConfigSyncOps
from .views import BindConfTagRelated

urlpatterns = [
    url(r'^bindconfig/generate$', BindConfigGenerateOps.as_view(), name='generate bind9 config'),
    url(r'^bindconfig/confsync$', BindConfigSyncOps.as_view(), name='sync bind9 config'),
    url(r'^bindconfig/relatedserver$', BindConfTagRelated.as_view(), name=' tag related server')
]
