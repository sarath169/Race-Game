from django.db import models
from django.contrib.auth.models import User

class GameDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=128)
    level = models.CharField(max_length=128)
    correct = models.CharField(max_length=128)
    wrong = models.CharField(max_length=128)
    streak = models.CharField(max_length=128)


    class Meta:
        db_table = "GameDetails"