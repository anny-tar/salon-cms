from django import forms
from django.contrib import admin
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin
from .models import SiteSettings, SitePage, Section, SectionStep


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'color_primary':    forms.TextInput(attrs={'type': 'color'}),
            'color_secondary':  forms.TextInput(attrs={'type': 'color'}),
            'color_accent':     forms.TextInput(attrs={'type': 'color'}),
            'color_background': forms.TextInput(attrs={'type': 'color'}),
        }


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm
    save_on_top = True
    fieldsets = (
        ('Основное', {
            'fields': ('salon_name', 'phone', 'email', 'address', 'logo', 'favicon'),
        }),
        ('Брендинг', {
            'fields': ('color_primary', 'color_secondary', 'color_accent', 'color_background', 'font'),
        }),
        ('Водяной знак на фото', {
            'fields': ('watermark_type', 'watermark_text', 'watermark_opacity'),
        }),
        ('Документы', {
            'fields': ('privacy_policy',),
        }),
        ('SEO главной страницы', {
            'fields': ('seo_title', 'meta_description', 'robots'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SitePage)
class SitePageAdmin(OrderedModelAdmin):
    list_display       = ('nav_label', 'slug', 'is_visible', 'move_up_down_links')
    list_display_links = ('nav_label',)
    ordering           = ('order',)
    fields             = ('page_type', 'nav_label', 'slug', 'is_visible', 'seo_title', 'meta_description')
    readonly_fields    = ('page_type',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SectionStepInline(admin.TabularInline):
    model    = SectionStep
    extra    = 1
    fields   = ('order', 'number', 'text')
    ordering = ('order',)
    verbose_name = 'Шаг'
    verbose_name_plural = 'Шаги (добавьте нужное количество)'


@admin.register(Section)
class SectionAdmin(OrderedModelAdmin):
    list_display       = ('icon_and_name', 'anchor', 'is_visible', 'move_up_down_links')
    list_display_links = ('icon_and_name',)
    ordering           = ('order',)

    def get_inlines(self, request, obj=None):
        if obj and obj.type == 'steps':
            return [SectionStepInline]
        return []

    def get_fields(self, request, obj=None):
        if obj is None:
            return ('site', 'type')
        if obj.type in ('banner', 'text_image'):
            return ('site', 'type', 'image', 'settings', 'anchor', 'is_visible')
        return ('site', 'type', 'settings', 'anchor', 'is_visible')

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('site', 'type')
        return ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_visible = False
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order')

    @admin.display(description='Секция')
    def icon_and_name(self, obj):
        return format_html(
            '<span style="font-size:16px;margin-right:8px;">{}</span><strong>{}</strong>',
            obj.icon,
            obj.get_type_display(),
        )

    class Media:
        js = ('site_constructor/section_edit.js',)