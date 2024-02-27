from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Patient


class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'required': True}))
    email = forms.EmailField(
        max_length=100, widget=forms.TextInput(attrs={'required': True}))

    image = forms.ImageField(required=True)
    phone = forms.CharField(
        max_length=11, widget=forms.TextInput(attrs={'required': True}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',
                  'image', 'phone']

    def save(self, commit=True):
        patient = super().save(commit=False)
        patient.user_type = 'Patient'
        if commit:
            patient.save()

            image = self.cleaned_data.get('image')
            phone = self.cleaned_data.get('phone')

            Patient.objects.create(user=patient, image=image, phone=phone)

        return patient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-100 border border-gray-300 rounded py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                )
            })
