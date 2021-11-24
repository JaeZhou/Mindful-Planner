from django.contrib.auth.models import AbstractUser
from django.db import models

class Notification(models.Model):
    msg = models.TextField()
    time = models.DateTimeField()
    sent = models.BooleanField(default=False)
