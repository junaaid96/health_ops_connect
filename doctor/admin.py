from django.contrib import admin
from .models import Expertise, Designation, AvailableTime, Doctor, Review

# Register your models here.


class ExpertiseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class DesignationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'fee')
    list_filter = ('expertise', 'designation', 'available_time')
    search_fields = ('user__username', 'user__first_name',
                     'user__last_name')

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'doctor', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer', 'doctor', 'rating', 'created_at')


admin.site.register(Expertise, ExpertiseAdmin)
admin.site.register(Designation, DesignationAdmin)
admin.site.register(AvailableTime)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Review, ReviewAdmin)
