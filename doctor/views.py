from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import FormView, ListView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import DoctorRegistrationForm
from .models import Doctor, Review
from appointment.models import Appointment
from patient.models import Patient
from patient.forms import PatientProfileUpdateForm
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


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

    # check user is patient or doctor before logging in
    def form_valid(self, form):
        user = form.get_user()
        if hasattr(user, 'doctor'):
            login(self.request, user)
            return redirect('doctor_profile')
        else:
            messages.error(
                self.request, 'No doctor account found with the provided credentials. Try patient login instead.')
            return redirect('doctor_login')

    def get_success_url(self):
        return reverse_lazy('doctor_profile')


class DoctorProfileView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'doctor_profile.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.user.doctor)

    # count of pending, completed, cancelled and running appointments
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending'] = Appointment.objects.filter(
            doctor=self.request.user.doctor, appointment_status='Pending').count()
        context['completed'] = Appointment.objects.filter(
            doctor=self.request.user.doctor, appointment_status='Completed').count()
        context['cancelled'] = Appointment.objects.filter(
            doctor=self.request.user.doctor, appointment_status='Cancelled').count()
        context['running'] = Appointment.objects.filter(
            doctor=self.request.user.doctor, appointment_status='Running').count()
        return context

# doctor can change patient's appointment status


def change_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.appointment_status = request.POST['status']
        appointment.save()

        mail_subject = f"Your Appointment is {appointment.appointment_status}!"
        mail_body = render_to_string('email/appointment_status_email.html', {
            'patient': appointment.patient,
            'doctor': appointment.doctor,
            'appointment': appointment
        })
        email = EmailMultiAlternatives(
            mail_subject, '', to=[appointment.patient.user.email])
        email.attach_alternative(mail_body, "text/html")
        email.send()

        messages.success(request, 'Appointment status updated successfully')
        return redirect('doctor_profile')
    return redirect('doctor_profile')


class DoctorLogoutView(LogoutView):
    next_page = 'doctor_login'


class DoctorDetailsView(DetailView):
    model = Doctor
    template_name = 'doctor_details.html'
    context_object_name = 'doctor'
    # form_class = DoctorReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(doctor=self.object)
        context['doctor'] = self.object
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'patient'):
                appointment = Appointment.objects.filter(
                    patient=self.request.user.patient, doctor=self.object).first()
                context['appointment'] = appointment
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 'You need to be logged in to add a review.')
            return redirect('patient_login')
        if Appointment.objects.filter(patient=request.user.patient, doctor=self.kwargs['pk']).exists():
            doctor = Doctor.objects.get(pk=self.kwargs['pk'])
            patient = request.user.patient
            body = request.POST['body']
            rating = request.POST['rating']
            Review.objects.create(
                reviewer=patient, doctor=doctor, body=body, rating=rating)
            messages.success(request, 'Review added successfully')
            return redirect('doctor_details', pk=self.kwargs['pk'])
        else:
            messages.error(
                request, 'You can only review doctors you have appointments with.')
            return redirect('patient_login')


class PatientProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'patient_details.html'

    def get(self, request, patient_username):
        if not hasattr(request.user, 'doctor'):
            return HttpResponse("Only doctor can update any patient's profile.")

        patient = get_object_or_404(Patient, user__username=patient_username)
        form = PatientProfileUpdateForm(instance=patient)
        return render(request, self.template_name, {'form': form})

    def post(self, request, patient_username):
        patient = get_object_or_404(Patient, user__username=patient_username)
        form = PatientProfileUpdateForm(
            request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.instance.user = patient.user
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('doctor_profile')
        return render(request, self.template_name, {'form': form})
