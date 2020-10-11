# -*- encoding: utf-8 -*-
# File    : urls.py
# Time    : 2020/6/30 10:41 AM
# Author  : ops

from django.conf.urls import url
from .views import BindServerListView
from .views import BindServerOpsView

urlpatterns = [
    url(r'^bindserver/list$', BindServerListView.as_view(), name='bind server list'),
    url(r'^bindserver/list/(?P<obj_id>\d+)/$', BindServerOpsView.as_view(), name='bind server ops')
]


# GET http://localhost:8000/api/bindserver/list/
# GET、DELETE http://localhost:8000/api/bindserver/list/4/
