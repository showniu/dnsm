from django.urls import re_path
from base.views import DoInfoAPIView

urlpatterns = [
    re_path(r'^api/auth/info', DoInfoAPIView.as_view()),

]
