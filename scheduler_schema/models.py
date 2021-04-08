from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime 

# Create your models here.


# This app uses default Django user Model


# A field validater for determinig if the date entered is a future date or not (Only allows future dates)
def validate_datetime(value):

    if value < ( timezone.now() - datetime.timedelta(seconds=2) ) : # Compensating 2 seconds for network or user-action latency
        raise ValidationError("You can not schedule an event for the past!")
    return value
    

# Schedule Model/Table 
class Schedule(models.Model):

    start_date_time = models.DateTimeField(blank=False, null=False, validators=[validate_datetime])
    end_date_time = models.DateTimeField(blank=False, null=False, validators=[validate_datetime])

    title = models.CharField(max_length=100, blank=False, null=False)
    users = models.ManyToManyField(User, related_name='scheduled_events', blank=False)

    def __str__(self):
        return f"{self.title}"


# Proxying Django User Model to check if the user is available at the provided date and time

class UserAvailibility(User):

    class Meta:
        proxy = True

    """
    The following method returns the email of the user who has a scheduler conflict meaning
    that the user has other events scheduled at the given timings
    """
    def userNotAvailable(self, start_date_time, end_date_time):

        users_scheduled_events = self.scheduled_events.filter(start_date_time__gte=start_date_time,
                                                              end_date_time__lte=end_date_time)
        if users_scheduled_events:
            return self.email
