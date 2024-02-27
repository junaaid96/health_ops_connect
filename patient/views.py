from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import PatientRegistrationForm

class PatientRegistrationView(FormView):
    template_name = 'patient_register.html'
    form_class = PatientRegistrationForm
    success_url = reverse_lazy('patient_login')

    def form_valid(self, form):
        doctor = form.save()
        messages.success(self.request, 'Account created successfully')
        login(self.request, doctor)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # check if user is logged in when trying to access the registration page
            return redirect('patient_profile')  # redirect to profile page
        return super().dispatch(request, *args, **kwargs)
    
class PatientLoginView(LoginView):
    template_name = 'patient_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('patient_profile')