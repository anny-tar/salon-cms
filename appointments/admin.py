from django.contrib import admin
from django.utils.html import format_html
from .models import Appointment, AppointmentReferencePhoto

STATUS_COLORS = {
    'pending':     {'bg': '#FFC107', 'color': '#fff', 'label': 'Ожидает подтверждения'},
    'confirmed':   {'bg': '#198754', 'color': '#fff', 'label': 'Подтверждена'},
    'in_progress': {'bg': '#0D6EFD', 'color': '#fff', 'label': 'В процессе'},
    'completed':   {'bg': '#6C757D', 'color': '#fff', 'label': 'Завершена'},
    'no_show':     {'bg': '#fd7e14', 'color': '#fff', 'label': 'Не явился'},
    'cancelled':   {'bg': '#DC3545', 'color': '#fff', 'label': 'Отменена'},
}


class ReferencePhotoInline(admin.TabularInline):
    model  = AppointmentReferencePhoto
    extra  = 0
    fields = ('photo', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    verbose_name = 'Референс'
    verbose_name_plural = 'Фото-референсы клиента'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display    = ('date', 'time_start', 'time_end', 'client', 'specialist', 'service', 'colored_status')
    list_filter     = ('status', 'date', 'specialist')
    search_fields   = ('client__full_name', 'client__phone', 'specialist__full_name')
    readonly_fields = ('time_end', 'created_at', 'updated_at')
    date_hierarchy  = 'date'
    inlines         = [ReferencePhotoInline]

    def colored_status(self, obj):
        s     = STATUS_COLORS.get(obj.status, {})
        label = obj.get_status_display()
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:12px;font-size:12px;font-weight:500;">{}</span>',
            s.get('bg', '#fff'), s.get('color', '#000'), label,
        )
    colored_status.short_description = 'Статус'