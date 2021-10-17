from django.db import models
from accounts.models import User

# Create your models here.

#Task model
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(auto_now_add=False, blank=False)
    due_time = models.TimeField(auto_now_add=False, blank=False)

    # class Meta:
    #     order_with_respect_to = "due_date"
    #     order_with_respect_to = "due_time"

    def __str__(self):
        return self.name