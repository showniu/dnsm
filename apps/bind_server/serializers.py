# -*- encoding: utf-8 -*-
# File    : serializers.py
# Time    : 2020/6/30 10:17 AM
# Author  : ops

from rest_framework import serializers
from .models import t_bindserver

class BindServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_bindserver
        fields = '__all__'

    # def create(self, validated_data):
    #     return t_bindserver.objects.create(**validated_data)
