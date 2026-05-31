from django.contrib import admin
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin
from .models import SiteSettings, Section


class SectionInline(OrderedStackedInline):
    model = Section
    fields = ('type', 'settings', 'order', 'move_up_down_links')
    readonly_fields = ('order', 'move_up_down_links')
    extra = 0
    ordering = ('order',)

    class Media:
        js = ('site_constructor/section_admin.js',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    inlines = [SectionInline]

    fieldsets = (
        ('Основное', {
            'fields': ('salon_name', 'phone', 'email', 'address', 'logo', 'favicon')
        }),
        ('Страницы сайта', {
            'fields': ('show_services', 'show_team', 'show_portfolio', 'show_news', 'show_products')
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