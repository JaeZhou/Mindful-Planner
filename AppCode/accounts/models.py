from django.contrib.auth.models import AbstractUser
from django.db import models

# Set up DB tables and those kinds of things

class User(AbstractUser):
    #email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
       return self.username