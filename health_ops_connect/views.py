from django.views.generic import ListView
from doctor.models import Doctor, Expertise


class DoctorListView(ListView):
    model = Doctor
    template_name = 'home.html'
    context_object_name = 'doctors'

    def get_queryset(self):
        expertise_slug = self.kwargs.get('expertise')
        if expertise_slug:
            expertise = Expertise.objects.get(
                slug=expertise_slug)
            return Doctor.objects.filter(expertise=expertise)
        return Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expertises'] = Expertise.objects.all()
        return context


# class FilterDoctorListView(ListView):
#     model = Doctor
#     template_name = 'home.html'
#     context_object_name = 'doctors'

#     def get_queryset(self):
#         return Doctor.objects.filter(specialization__slug=self.kwargs['specialization'])
