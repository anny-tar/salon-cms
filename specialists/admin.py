from django.contrib import admin
from django.contrib import messages
from portfolio.models import PortfolioWork
from .models import Specialist, SpecialistDocument


class SpecialistDocumentInline(admin.TabularInline):
    model = SpecialistDocument
    extra = 1
    fields = ('title', 'file')


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'is_active', 'portfolio_count')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'specialization')
    list_editable = ('is_active',)
    inlines = [SpecialistDocumentInline]
    actions = ['hide_portfolio', 'show_portfolio']

    fieldsets = (
        ('Основное', {
            'fields': ('user', 'full_name', 'specialization', 'photo', 'description', 'is_active')
        }),
        ('Расписание', {
            'fields': ('work_schedule',),
            'description': 'Пример: {"mon": ["09:00","20:00"], "wed": ["10:00","18:00"]}'
        }),
    )

    def portfolio_count(self, obj):
        visible = PortfolioWork.objects.filter(specialist=obj, is_visible=True).count()
        total = PortfolioWork.objects.filter(specialist=obj).count()
        return f'{visible} / {total}'
    portfolio_count.short_description = 'Работ (видно/всего)'

    @admin.action(description='Скрыть все работы с сайта')
    def hide_portfolio(self, request, queryset):
        for specialist in queryset:
            count = PortfolioWork.objects.filter(
                specialist=specialist, is_visible=True
            ).update(is_visible=False)
        self.message_user(request, 'Работы скрыты с публичного сайта', messages.SUCCESS)

    @admin.action(description='Показать все работы на сайте')
    def show_portfolio(self, request, queryset):
        for specialist in queryset:
            PortfolioWork.objects.filter(
                specialist=specialist, is_visible=False
            ).update(is_visible=True)
        self.message_user(request, 'Работы снова видны на сайте', messages.SUCCESS)