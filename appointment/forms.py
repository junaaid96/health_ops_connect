from django import forms
from .models import Appointment
from doctor.models import Doctor


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_type', 'symptoms', 'appointment_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
