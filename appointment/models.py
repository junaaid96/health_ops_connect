from django.db import models
from patient.models import Patient
from doctor.models import Doctor, AvailableTime
from health_ops_connect.constants import APPOINTMENT_TYPE, APPOINTMENT_STATUS

# Create your models here.


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(
        choices=APPOINTMENT_TYPE, max_length=10)
    appointment_status = models.CharField(
        choices=APPOINTMENT_STATUS, max_length=10, default='Pending')
    symptoms = models.TextField()
    appointment_time = models.ForeignKey(
        AvailableTime, on_delete=models.CASCADE)
    cancellation = models.BooleanField(default=False)

    def __str__(self):
        return f"Patient: {self.patient.user.first_name} - Doctor: {self.doctor.user.first_name}"
