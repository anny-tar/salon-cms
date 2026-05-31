from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Основное', {
            'fields': ('salon_name', 'phone', 'email', 'address', 'logo', 'favicon')
        }),
        ('Брендинг', {
            'fields': ('color_primary', 'color_secondary', 'color_accent', 'color_background', 'font')
        }),
        ('Баннер', {
            'fields': ('banner_title', 'banner_subtitle', 'banner_image', 'banner_cta_text')
        }),
        ('Блок текст + фото', {
            'fields': ('text_image_title', 'text_image_body', 'text_image_photo'),
            'classes': ('collapse',),
        }),
        ('Шаги', {
            'fields': ('steps_title', 'steps_config'),
            'classes': ('collapse',),
        }),
        ('Таблица', {
            'fields': ('table_title', 'table_config'),
            'classes': ('collapse',),
        }),
        ('Водяной знак', {
            'fields': ('watermark_type', 'watermark_text', 'watermark_opacity')
        }),
        ('Документы', {
            'fields': ('privacy_policy',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False