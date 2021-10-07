from django.db import models
from django.contrib.auth.models import User

class GameDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    level = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    streak = models.PositiveIntegerField()


    class Meta:
        db_table = "GameDetails"