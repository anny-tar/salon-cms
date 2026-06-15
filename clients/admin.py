from django import forms
from django.contrib import admin
from .models import Client, ClientTag


@admin.register(ClientTag)
class ClientTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_count')
    search_fields = ('name',)

    def client_count(self, obj):
        return obj.clients.count()
    client_count.short_description = 'Клиентов'


class ClientAdminForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 000-00-00',
            'data-mask': '+7 (000) 000-00-00',
        })
    )
    class Meta:
        model = Client
        fields = '__all__'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm

    class Media:
        js = ('https://cdn.jsdelivr.net/npm/imask@7.6.1/dist/imask.min.js',
              'js/phone_mask.js')
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