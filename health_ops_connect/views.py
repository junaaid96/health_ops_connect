from django.views.generic import ListView
from doctor.models import Doctor, Specialization


class DoctorListView(ListView):
    model = Doctor
    template_name = 'home.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        specialization_slug = self.kwargs.get('specialization')
        if specialization_slug:
            specialization = Specialization.objects.get(
                slug=specialization_slug)
            return Doctor.objects.filter(specialization=specialization)
        return Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context


# class FilterDoctorListView(ListView):
#     model = Doctor
#     template_name = 'home.html'
#     context_object_name = 'doctors'

#     def get_queryset(self):
#         return Doctor.objects.filter(specialization__slug=self.kwargs['specialization'])
