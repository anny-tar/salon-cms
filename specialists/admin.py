from django.contrib import admin
from .models import Specialist


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'specialization')
    list_editable = ('is_active',)