from django.contrib import admin
from django.utils.html import format_html
from .models import Appointment


STATUS_COLORS = {
    'pending':     {'bg': '#FFF3CD', 'color': '#856404', 'label': 'Ожидает подтверждения'},
    'confirmed':   {'bg': '#D1E7DD', 'color': '#0F5132', 'label': 'Подтверждена'},
    'in_progress': {'bg': '#CCE5FF', 'color': '#004085', 'label': 'В процессе'},
    'completed':   {'bg': '#E2E3E5', 'color': '#383D41', 'label': 'Завершена'},
    'no_show':     {'bg': '#FFE5CC', 'color': '#7A3E00', 'label': 'Не явился'},
    'cancelled':   {'bg': '#F8D7DA', 'color': '#721C24', 'label': 'Отменена'},
}


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time_start', 'time_end', 'client', 'specialist', 'service', 'colored_status')
    list_filter = ('status', 'date', 'specialist')
    search_fields = ('client__full_name', 'client__phone', 'specialist__full_name')
    readonly_fields = ('time_end', 'created_at')
    date_hierarchy = 'date'

    def colored_status(self, obj):
        s = STATUS_COLORS.get(obj.status, {})
        bg = s.get('bg', '#fff')
        color = s.get('color', '#000')
        label = s.get('label', obj.status)
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:12px;font-size:12px;font-weight:500;">{}</span>',
            bg, color, label
        )
    colored_status.short_description = 'Статус'