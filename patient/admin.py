from django.contrib import admin
from .models import Patient

# Register your models here.


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'image')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name', 'phone')
    list_filter = ('user__is_active', 'user__is_staff')

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


admin.site.register(Patient, PatientAdmin)
