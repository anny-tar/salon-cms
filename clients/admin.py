from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'pd_consent', 'created_at')
    list_filter = ('pd_consent',)
    search_fields = ('full_name', 'phone', 'email')
    readonly_fields = ('created_at', 'pd_consent_datetime')