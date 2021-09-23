from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers

from .models import GameDetail

class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameDetail
        fields = ('user', 'score', 'level', 'correct', 'wrong', 'streak')