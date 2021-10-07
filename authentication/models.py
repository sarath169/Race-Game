from django.db import models
from django.contrib.auth.models import User

class UserOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    
    class Meta:
        db_table = "UserOtps"