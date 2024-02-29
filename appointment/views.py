from django.shortcuts import render
from django.views.generic import CreateView
from .models import Appointment
from .forms import AppointmentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from patient.models import Patient
from django.contrib import messages

# Create your views here.


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'take_appointment.html'

    def form_valid(self, form):
        patient = Patient.objects.get(user=self.request.user)

        if patient is None:
            return HttpResponse('You are not a patient', status=400)

        if patient.appointment_set.filter(appointment_time=form.instance.appointment_time).exists() and Appointment.objects.filter(appointment_status='Pending').exists():
            messages.error(
                self.request, 'You already have an appointment at this time!')
            return super().form_invalid(form)

        form.instance.patient = patient
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient_profile')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({'doctor_id': self.kwargs['doctor_id']})
    #     return kwargs
