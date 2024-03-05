from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import PatientRegistrationForm
from appointment.models import Appointment
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse


class PatientRegistrationView(FormView):
    template_name = 'patient_register.html'
    form_class = PatientRegistrationForm
    success_url = reverse_lazy('patient_login')

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request, 'Account created. Check your email to activate your account.')

        # send email to user to activate account
        token = default_token_generator.make_token(user)
        print("token: ", token)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print("uid: ", uid)

        confirmation_url = f"https://health-ops-connect-mvt.onrender.com/patients/activate/{
            uid}/{token}/"

        mail_subject = "Activate Your Account"
        mail_body = render_to_string('email/activation_email.html', {
            'user': user,
            'confirmation_url': confirmation_url
        })
        email = EmailMultiAlternatives(
            mail_subject, '', to=[user.email])
        email.attach_alternative(mail_body, "text/html")
        email.send()

        return super().form_valid(form)

    def activate_account(self, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # messages.success(request, 'Account activated successfully. You can now login.')
            return redirect('patient_login')
        else:
            # messages.error(request, 'Activation link is invalid or has expired.')
            return HttpResponse('Activation link is invalid or has expired.')

    def form_invalid(self, form):
        messages.error(
            self.request, 'Account creation failed. Please correct the errors below.')
        return super().form_invalid(form)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed'] = Appointment.objects.filter(
            patient=self.request.user.patient, appointment_status='Completed').count()
        return context

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
