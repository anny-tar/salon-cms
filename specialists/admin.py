from django.contrib import admin
from .models import Specialist, SpecialistDocument


class SpecialistDocumentInline(admin.TabularInline):
    model = SpecialistDocument
    extra = 1
    fields = ('title', 'file')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'specialization')
    list_editable = ('is_active',)
    inlines = [SpecialistDocumentInline]
    fieldsets = (
        ('Основное', {
            'fields': ('user', 'full_name', 'specialization', 'photo', 'description', 'is_active')
        }),
        ('Расписание', {
            'fields': ('work_schedule',),
            'description': 'Пример: {"mon": ["09:00","20:00"], "wed": ["10:00","18:00"]}'
        }),
    )