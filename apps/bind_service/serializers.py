# -*- encoding: utf-8 -*-
# File    : serializers.py
# Time    : 2020/7/6 10:45 上午
# Author  : ops
from rest_framework import serializers
from .models import t_bindservice_zone
from .models import t_bindservice_aclView
from .models import t_bindservice_record

class BindAclViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_bindservice_aclView
        fields = '__all__'
    # def create(self, validated_data):
    #     return t_bindservice_aclView.objects.create(**validated_data)


class BindZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_bindservice_zone
        fields = '__all__'

    # def create(self, validated_data):
    #     return t_bindservice_zone.objects.create(**validated_data)


class BindRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = t_bindservice_record
        fields = '__all__'

    # def create(self, validated_data):
    #     return t_bindservice_record.objects.create(**validated_data)


