from django.db import models
from django.contrib.auth.models import AbstractUser
from users.choices import *

class CustomUser(AbstractUser):
    # add additional fields in here
    userType = models.IntegerField("User role", choices=USER_TYPES, default=1)
    # PIN = models.CharField(max_length=50,blank=True, default='Please input your PIN code')

