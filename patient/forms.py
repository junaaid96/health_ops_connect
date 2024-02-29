from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Patient
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


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
        patient.is_active = False
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

# class CustomAuthenticationForm(AuthenticationForm):
#     def confirm_login_allowed(self, user):
#         if not user.is_active:
#             raise forms.ValidationError("This account is inactive. Please activate it to log in.")


class PatientProfileUpdateForm(forms.ModelForm):
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
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'image', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-100 border border-gray-300 rounded py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                )
            })

            if self.instance:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email

                self.fields['image'].initial = self.instance.image
                self.fields['phone'].initial = self.instance.phone

    def save(self, commit=True):
        patient = super().save(commit=False)
        
        patient.user.first_name = self.cleaned_data.get('first_name')
        patient.user.last_name = self.cleaned_data.get('last_name')
        patient.user.email = self.cleaned_data.get('email')

        patient.image = self.cleaned_data.get('image')
        patient.phone = self.cleaned_data.get('phone')

        if commit:
            patient.user.save()
            patient.save()

        return patient
