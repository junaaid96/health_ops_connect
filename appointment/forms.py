from django import forms
from .models import Appointment
from doctor.models import AvailableTime, Doctor


class AppointmentForm(forms.ModelForm):
    appointment_time = forms.ModelChoiceField(
        queryset=AvailableTime.objects.none())

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_type', 'symptoms', 'appointment_time']

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if doctor:
            self.fields['appointment_time'].queryset = doctor.available_time.all()

        # if 'doctor_id' in kwargs:
        #     doctor_id = kwargs.pop('doctor_id')
        #     doctor = Doctor.objects.get(id=doctor_id)
        #     self.fields['appointment_time'].choices = doctor.get_appointment_time_choices()

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-100 border border-gray-300 rounded py-2 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500'
                )
            })
