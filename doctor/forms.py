from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Designation, Specialization, AvailableTime, Review
from health_ops_connect.constants import STAR_CHOICES


class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    email = forms.EmailField(
        max_length=100, widget=forms.TextInput(attrs={'required': True}))

    image = forms.ImageField(required=True)
    designation = forms.ModelMultipleChoiceField(
        queryset=Designation.objects.all(), required=True)
    specialization = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(), required=True)
    available_time = forms.ModelMultipleChoiceField(
        queryset=AvailableTime.objects.all(), required=True)
    fee = forms.IntegerField(required=True)
    meet_link = forms.URLField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', 'image', 'designation', 'specialization', 'available_time', 'fee', 'meet_link']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'Doctor'
        if commit:
            user.save()

            image = self.cleaned_data.get('image')
            fee = self.cleaned_data.get('fee')
            meet_link = self.cleaned_data.get('meet_link')

            doctor = Doctor.objects.create(user=user, image=image,
                                           fee=fee, meet_link=meet_link)

            designation = self.cleaned_data.get('designation')
            specialization = self.cleaned_data.get('specialization')
            available_time = self.cleaned_data.get('available_time')

            if designation:
                doctor.designation.set(designation)

            if specialization:
                doctor.specialization.set(specialization)

            if available_time:
                doctor.available_time.set(available_time)

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-100 border border-gray-300 rounded py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                )
            })


# class DoctorReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['body', 'rating']
