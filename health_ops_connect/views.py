from django.views.generic import ListView
from doctor.models import Doctor

class DoctorListView(ListView):
    model = Doctor
    template_name = 'home.html'
    context_object_name = 'doctors'
