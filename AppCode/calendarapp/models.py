from django.db import models
from accounts.models import User

# Create your models here.

#Calendar event model

class Event(models.Model):
    title = models.CharField(max_length=200)
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    startTime = models.TimeField(u'Starting time', help_text=u'Starting time', blank=True)
    endTime = models.TimeField(u'Ending time', help_text=u'Ending time', blank=True)
    description = models.TextField(u'Event description', help_text=u'Event description', blank=True, null=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title