from django.contrib import admin
from .models import Client, ClientTag


@admin.register(ClientTag)
class ClientTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_count')
    search_fields = ('name',)

    def client_count(self, obj):
        return obj.clients.count()
    client_count.short_description = 'Клиентов'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display   = ('full_name', 'phone', 'email', 'tag_list', 'created_at')
    search_fields  = ('full_name', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)
    list_filter    = ('tags',)

    fieldsets = (
        ('Основное', {
            'fields': ('full_name', 'phone', 'email'),
        }),
        ('Дополнительно', {
            'fields': ('tags', 'comment', 'created_at', 'updated_at'),
        }),
    )

    def tag_list(self, obj):
        return ', '.join(t.name for t in obj.tags.all()) or '—'
    tag_list.short_description = 'Теги'