from django.contrib import admin
from .models import PhotoConsent, PortfolioWork


@admin.register(PhotoConsent)
class PhotoConsentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(PortfolioWork)
class PortfolioWorkAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'service_category', 'work_date', 'source', 'is_visible')
    list_filter = ('is_visible', 'source', 'specialist')
    search_fields = ('specialist__full_name',)
    readonly_fields = ('photo_watermarked', 'liability_datetime')
    list_editable = ('is_visible',)