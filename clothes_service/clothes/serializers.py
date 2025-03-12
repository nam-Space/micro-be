from rest_framework import serializers
from .models import Clothes
from rest_framework import viewsets


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = "__all__"
