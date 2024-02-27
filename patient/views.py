from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import PatientRegistrationForm
from appointment.models import Appointment


class PatientRegistrationView(FormView):
    template_name = 'patient_register.html'
    form_class = PatientRegistrationForm
    success_url = reverse_lazy('patient_login')

    def form_valid(self, form):
        doctor = form.save()
        messages.success(self.request, 'Account created successfully!')
        login(self.request, doctor)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # check if user is logged in when trying to access the registration page
            return redirect('patient_profile')  # redirect to profile page
        return super().dispatch(request, *args, **kwargs)


class PatientLoginView(LoginView):
    template_name = 'patient_login.html'
    redirect_authenticated_user = True

    # check user is patient or doctor before logging in
    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'patient'):
            login(self.request, user)
            return redirect('patient_profile')
        else:
            messages.error(
                self.request, 'No patient account found with the provided credentials. Try doctor login instead.')
            return redirect('patient_login')

    def get_success_url(self):
        return reverse_lazy('patient_profile')


class PatientProfileView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'patient_profile.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.patient)


def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.cancellation = True
    appointment.appointment_status = 'Cancelled'
    appointment.save()
    messages.success(request, 'Appointment cancelled successfully')
    return redirect('patient_profile')


class PatientLogoutView(LogoutView):
    next_page = 'patient_login'
