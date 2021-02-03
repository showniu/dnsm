# -*- encoding: utf-8 -*-
# File    : urls.py
# Time    : 2020/6/30 10:41 AM
# Author  : ops

from django.conf.urls import url
from .views import BindServerListView
from .views import BindServerOpsView
from .views import BindServerInit
from .views import ResetBindServerInit
from .views import BindServerIPListView

urlpatterns = [
    url(r'^bindserver/list$', BindServerListView.as_view(), name='bind server list'),
    url(r'^bindserver/list/ip$', BindServerIPListView.as_view(), name='bind server ops for ip'),
    url(r'^bindserver/list/(?P<obj_id>\d+)/$', BindServerOpsView.as_view(), name='bind server ops'),
    url(r'^bindserver/init$', BindServerInit.as_view(), name='bind server init'),
    url(r'^bindserver/reststate/(?P<obj_id>\d+)/$', ResetBindServerInit.as_view(), name='reset server init')
]


# GET http://localhost:8000/api/bindserver/list/
# GET、DELETE http://localhost:8000/api/bindserver/list/4/
