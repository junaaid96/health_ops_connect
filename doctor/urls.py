from django.urls import path
from .views import DoctorRegistrationView, DoctorLoginView, DoctorLogoutView, DoctorProfileView, change_appointment_status, DoctorDetailsView, PatientProfileUpdateView

urlpatterns = [
    path('register/', DoctorRegistrationView.as_view(), name='doctor_register'),
    path('login/', DoctorLoginView.as_view(), name='doctor_login'),
    path('profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('change-status/<int:pk>/', change_appointment_status,
         name='change_appointment_status'),
    path('logout/', DoctorLogoutView.as_view(), name='doctor_logout'),
    path('details/<int:pk>/', DoctorDetailsView.as_view(), name='doctor_details'),
    path('update-patient-profile/<str:patient_username>', PatientProfileUpdateView.as_view(),
         name='patient_profile_update'),
]
