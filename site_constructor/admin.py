from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin
from .models import SiteSettings, Section


class SectionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = Section
    extra = 0
    fields = ('type', 'settings', 'order')
    readonly_fields = ()

    class Media:
        js = ('site_constructor/section_admin.js',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [SectionInline]

    fieldsets = (
        ('Основное', {
            'fields': ('salon_name', 'phone', 'email', 'address', 'logo', 'favicon')
        }),
        ('Брендинг', {
            'fields': ('color_primary', 'color_secondary', 'color_accent', 'color_background', 'font')
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