from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime 

# Create your models here.


# This app uses default Django user Model




# A filed validater for determinig if the date entered is a future date or not (Only allows future dates)
def validate_datetime(value):
    if value < ( timezone.now() - datetime.timedelta(seconds=2) ) : # Compensating 2 seconds for network or user-action latency
        raise ValidationError("You can not schedule an event for the past!")
    return value
    

# The Schedule Model/Table 
class Schedule(models.Model):

    date_time = models.DateTimeField(blank=False, null=False, validators=[validate_datetime])
    title = models.CharField(max_length=100, blank=False, null=False)
    users = models.ManyToManyField(User, related_name='scheduled_events', blank=False)

    def __str__(self):
        return f"{self.title}"