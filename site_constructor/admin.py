from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('salon_name', 'phone', 'address')
    readonly_fields = ()

    fieldsets = (
        ('Основное', {
            'fields': ('salon_name', 'phone', 'address', 'logo', 'favicon')
        }),
        ('Брендинг', {
            'fields': (
                'color_primary', 'color_secondary',
                'color_accent', 'color_background', 'font'
            )
        }),
        ('Водяной знак', {
            'fields': ('watermark_type', 'watermark_text', 'watermark_opacity')
        }),
        ('Документы', {
            'fields': ('privacy_policy',)
        }),
    )

    def has_add_permission(self, request):
        # Запрещаем создание второй записи
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление
        return False