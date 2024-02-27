from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import DoctorRegistrationForm
from appointment.models import Appointment


class DoctorRegistrationView(FormView):
    template_name = 'doctor_register.html'
    form_class = DoctorRegistrationForm
    success_url = reverse_lazy('doctor_login')

    def form_valid(self, form):
        doctor = form.save()
        messages.success(self.request, 'Account created successfully')
        login(self.request, doctor)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # check if user is logged in when trying to access the registration page
            return redirect('doctor_profile')  # redirect to profile page
        return super().dispatch(request, *args, **kwargs)


class DoctorLoginView(LoginView):
    template_name = 'doctor_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('doctor_profile')


class DoctorProfileView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'doctor_profile.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user.doctor)

# doctor can change patient's appointment status
def change_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.appointment_status = request.POST['status']
        appointment.save()
        messages.success(request, 'Appointment status updated successfully')
        return redirect('doctor_profile')
    return redirect('doctor_profile')


class DoctorLogoutView(LogoutView):
    next_page = 'doctor_login'
