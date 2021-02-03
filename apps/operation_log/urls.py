# -*- encoding: utf-8 -*-
# File    : urls.py.py
# Time    : 2020/11/27 下午4:27
# Author  : ops
from django.conf.urls import url
from .views import OperationsLog

urlpatterns = [
    url(r'^oplog/$', OperationsLog.as_view(), name='bind operations log'),
]
