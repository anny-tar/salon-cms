from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time_start', 'time_end', 'client', 'specialist', 'service', 'status')
    list_filter = ('status', 'date', 'specialist')
    search_fields = ('client__full_name', 'client__phone', 'specialist__full_name')
    readonly_fields = ('time_end', 'created_at')
    date_hierarchy = 'date'