# -*- encoding: utf-8 -*-
# File    : setializers.py
# Time    : 2020/12/18 下午5:12
# Author  : ops

from rest_framework import serializers
from .models import t_bindconf_tag

class BindConfTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_bindconf_tag
        fields = '__all__'
