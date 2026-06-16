from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin, OrderedTabularInline, OrderedTabularInline
from .models import SiteSettings, SitePage, Section, SectionStep, Contact, Address, Address
from .section_forms import get_section_form


# ── SiteSettings ──────────────────────────────────────────────────────

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
        ('Яндекс SmartCaptcha', {
            'fields': ('captcha_client_key', 'captcha_server_key'),
            'description': 'Ключи из Яндекс Cloud. Оставьте пустыми чтобы отключить капчу.',
        }),
        ('SEO главной страницы', {
            'fields': ('seo_title', 'meta_description', 'robots'),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── SitePage ──────────────────────────────────────────────────────────

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


# ── SectionStep inline ────────────────────────────────────────────────

class SectionStepInline(admin.TabularInline):
    model    = SectionStep
    extra    = 1
    fields   = ('number', 'text')
    ordering = ('id',)
    verbose_name = 'Шаг'
    verbose_name_plural = 'Шаги (добавьте нужное количество)'


# ── Section ───────────────────────────────────────────────────────────

@admin.register(Section)
class SectionAdmin(OrderedModelAdmin):
    list_display       = ('icon_and_name', 'anchor', 'is_visible', 'move_up_down_links')
    list_display_links = ('icon_and_name',)
    ordering           = ('order',)
    # settings исключён — рендерится через section_form в change_view
    exclude            = ('settings',)

    def get_inlines(self, request, obj=None):
        if obj and obj.type == 'steps':
            return [SectionStepInline]
        return []

    def get_fields(self, request, obj=None):
        if obj is None:
            return ('site', 'type')
        if obj.type in ('banner', 'text_image'):
            return ('site', 'type', 'image', 'anchor', 'is_visible')
        return ('site', 'type', 'anchor', 'is_visible')

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return ('site', 'type')
        return ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_visible = False
        super().save_model(request, obj, form, change)

        # Сохраняем настройки из section_form если объект уже существует
        if change and obj.pk:
            section_form = get_section_form(obj.type, data=request.POST)
            if section_form and section_form.is_valid():
                obj.settings = section_form.cleaned_data
                obj.save(update_fields=['settings'])

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        try:
            section = Section.objects.get(pk=object_id)
            section_form = get_section_form(
                section.type,
                data=request.POST if request.method == 'POST' else None,
                initial=section.settings,
            )
            extra_context['section_form']  = section_form
            extra_context['section_type']  = section.type
        except Section.DoesNotExist:
            pass
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.display(description='Секция')
    def icon_and_name(self, obj):
        return format_html(
            '<span style="font-size:16px;margin-right:8px;">{}</span><strong>{}</strong>',
            obj.icon,
            obj.get_type_display(),
        )


# ── Contact ──────────────────────────────────────────────────────

@admin.register(Contact)
class ContactAdmin(OrderedModelAdmin):
    list_display       = ('label', 'type', 'value', 'is_active', 'move_up_down_links')
    list_display_links = ('label',)
    list_filter        = ('type', 'is_active')
    ordering           = ('order',)
    fields             = ('type', 'label', 'value', 'is_active')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    fields       = ('name', 'address', 'map_url')