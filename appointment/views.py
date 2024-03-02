from django.shortcuts import render
from django.views.generic import CreateView
from .models import Appointment
from doctor.models import Doctor
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

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'doctor'):
            return HttpResponse('You are not allowed to take appointment as a doctor!')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = self.get_doctor()
        return context

    def get_form_kwargs(self):
        kwargs = super(AppointmentCreateView, self).get_form_kwargs()
        kwargs.update({'doctor': self.get_doctor()})
        return kwargs

    def get_doctor(self):
        return Doctor.objects.get(id=self.kwargs['doctor_id'])

    def form_valid(self, form):
        patient = Patient.objects.get(user=self.request.user)

        if Appointment.objects.filter(
            patient=patient,
            appointment_time=form.instance.appointment_time,
            appointment_status='Pending'
        ).exists():
            messages.error(
                self.request, 'You already have an appointment at this time!')
            return super().form_invalid(form)

        form.instance.patient = patient
        messages.success(self.request, 'Appointment taken successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('patient_profile')
