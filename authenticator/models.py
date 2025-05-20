from django.db import models
from django.contrib.auth.models import User #importing Predefined User table contains Username,firstname,lastname,email

# Creating models for authentication system

class customUser(User):
    phone = models.IntegerField()
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    otp = models.IntegerField(null=True,blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)

