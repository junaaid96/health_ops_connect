from django.urls import path
from .views import PatientRegistrationView, PatientLoginView, PatientProfileView, cancel_appointment, PatientLogoutView

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='patient_register'),
    path('activate/<uid64>/<token>/', PatientRegistrationView.activate_account, name='activate_account'),
    path('login/', PatientLoginView.as_view(), name='patient_login'),
    path('profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('cancel_appointment/<int:appointment_id>/',
         cancel_appointment, name='cancel_appointment'),
    path('logout/', PatientLogoutView.as_view(), name='patient_logout'),
]
