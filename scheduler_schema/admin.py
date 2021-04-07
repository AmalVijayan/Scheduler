from django.contrib import admin
from .models import Schedule
# Register your models here.

class ScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ('__str__', 'id', 'title', 'date_time',)

admin.site.register(Schedule, ScheduleAdmin)
