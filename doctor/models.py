from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from health_ops_connect.constants import STAR_CHOICES

# Create your models here.


class Specialization(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AvailableTime(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='doctor/media/uploads/', default='doctor/media/uploads/default.jpg')
    designation = models.ManyToManyField(Designation)
    specialization = models.ManyToManyField(Specialization)
    available_time = models.ManyToManyField(AvailableTime)
    fee = models.IntegerField()
    meet_link = models.URLField(max_length=200)
    user_type = models.CharField(
        default='Doctor', max_length=10, editable=False)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Review(models.Model):
    reviewer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.CharField(choices=STAR_CHOICES, max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient: {self.reviewer.user.first_name} {self.reviewer.user.last_name} - Doctor: {self.doctor.user.first_name} {self.doctor.user.last_name} - Rating: {self.rating}"
