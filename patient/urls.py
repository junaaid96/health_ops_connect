from django.urls import path
from .views import PatientRegistrationView, PatientLoginView

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='patient_register'),
    path('login/', PatientLoginView.as_view(), name='patient_login'),
]