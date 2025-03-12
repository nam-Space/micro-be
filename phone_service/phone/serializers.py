from rest_framework import serializers
from .models import Phone
from rest_framework import viewsets


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = "__all__"
