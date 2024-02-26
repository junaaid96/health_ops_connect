from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Designation, Specialization, AvailableTime


class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    email = forms.EmailField(
        max_length=100, widget=forms.TextInput(attrs={'required': True}))

    image = forms.ImageField(required=False)
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
        fields = ['username', 'first_name', 'last_name', 'username', 'email', 'password1',
                  'password2', 'image', 'designation', 'specialization', 'available_time', 'fee', 'meet_link']

    def save(self, commit=True):
        doctor = super().save(commit=False)
        doctor.user_type = 'Doctor'
        if commit:
            doctor.save()

            image = self.cleaned_data.get('image')
            designation = self.cleaned_data.get('designation')
            specialization = self.cleaned_data.get('specialization')
            available_time = self.cleaned_data.get('available_time')
            fee = self.cleaned_data.get('fee')
            meet_link = self.cleaned_data.get('meet_link')

            doctor = Doctor.objects.create(
                user=doctor, image=image, designation=designation, specialization=specialization, available_time=available_time, fee=fee, meet_link=meet_link)

        return doctor

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-100 border border-gray-300 rounded py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                )
            })

