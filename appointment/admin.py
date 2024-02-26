from django.contrib import admin
from .models import Appointment

# Register your models here.


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'appointment_type',
                    'appointment_status', 'appointment_time', 'cancellation')
    list_filter = ('appointment_status', 'appointment_type', 'cancellation')
    search_fields = ('patient', 'doctor', 'appointment_status',
                     'appointment_type', 'cancellation')


admin.site.register(Appointment, AppointmentAdmin)
