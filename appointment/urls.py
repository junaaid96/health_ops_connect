from django.urls import path
from .views import AppointmentCreateView

urlpatterns = [
    path('take_appointment/', AppointmentCreateView.as_view(), name='take_appointment'),
]