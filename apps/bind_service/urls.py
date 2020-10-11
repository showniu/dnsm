# -*- encoding: utf-8 -*-
# File    : urls.py
# Time    : 2020/7/6 10:44 上午
# Author  : ops

from django.conf.urls import url
from .views import BindAclViewList
from .views import BindZonelist
from .views import BindRecordlist

from .views import BindAclViewOps
from .views import BindZoneOps
from .views import BindRecordOps
from .views import BindRecordSearch


urlpatterns = [
    url(r'^bindservice/aclview/list$', BindAclViewList.as_view(), name='bind aclview list'),
    url(r'^bindservice/aclview/list/(?P<obj_id>\d+)$', BindAclViewOps.as_view(), name='bind aclview detail'),
    url(r'^bindservice/zone/list$', BindZonelist.as_view(), name='bind zone list'),
    url(r'^bindservice/zone/list/(?P<obj_id>\d+)$', BindZoneOps.as_view(), name='bind zone detail'),
    # url(r'^bindservice/record/list$', BindRecordlist.as_view(), name='bind record list'),
    url(r'^bindservice/record/list$', BindRecordSearch.as_view(), name='bind record list'),
    # url(r'^bindservice/record/list(?P<record_key>.+)/$', BindRecordSearch.as_view(), name='bind record list search'),
    url(r'^bindservice/record/list/(?P<obj_id>\d+)$', BindRecordOps.as_view(), name='bind record detail')
]

# GET http://localhost:8000/bindservice/aclview/list
# GET、DELETE http://localhost:8000/api/bindservice/aclview/list/1