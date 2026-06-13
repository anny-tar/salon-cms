import logging
from django import forms
from django.contrib import admin, messages
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from portfolio.models import PortfolioWork
from .models import (
    Specialist, SpecialistDocument,
    SpecialistWorkDay, SpecialistScheduleException,
)
from .forms import SpecialistAdminForm

logger = logging.getLogger(__name__)


# ── Inlines ───────────────────────────────────────────────────────────

class SpecialistWorkDayInline(admin.TabularInline):
    model  = SpecialistWorkDay
    extra  = 0
    fields = ('weekday', 'time_start', 'time_end')
    verbose_name = 'Рабочий день'
    verbose_name_plural = 'Базовое расписание'

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('weekday')


class ScheduleExceptionInlineForm(forms.ModelForm):
    class Meta:
        model  = SpecialistScheduleException
        fields = '__all__'
        widgets = {
            'date':       forms.DateInput(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(attrs={'type': 'time'}),
            'time_end':   forms.TimeInput(attrs={'type': 'time'}),
            'comment':    forms.TextInput(attrs={
                'placeholder': 'Например: больничный, корпоратив, отпуск',
                'style': 'width:280px;',
            }),
        }


class ScheduleExceptionInline(admin.StackedInline):
    model   = SpecialistScheduleException
    form    = ScheduleExceptionInlineForm
    extra   = 1
    ordering = ('date',)
    verbose_name = 'Исключение'
    verbose_name_plural = (
        'Исключения в расписании '
    )
    fields = ('date', 'time_start', 'time_end', 'comment')

    def get_extra(self, request, obj=None, **kwargs):
        return 2 if obj is None else 1


class SpecialistDocumentInline(admin.TabularInline):
    model  = SpecialistDocument
    extra  = 1
    fields = ('title', 'file')
    verbose_name = 'Документ'
    verbose_name_plural = 'Документы об образовании'


# ── SpecialistAdmin ───────────────────────────────────────────────────

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    form = SpecialistAdminForm

    list_display  = ('full_name', 'specialization', 'schedule_summary', 'is_active', 'portfolio_count')
    list_filter   = ('is_active',)
    search_fields = ('full_name', 'specialization')
    list_editable = ('is_active',)
    inlines       = [SpecialistDocumentInline, SpecialistWorkDayInline, ScheduleExceptionInline]
    actions       = ['hide_portfolio', 'show_portfolio']

    fieldsets = (
        ('Основное', {
            'fields': ('user', 'full_name', 'specialization', 'photo', 'description', 'is_active'),
        }),
        ('Услуги специалиста', {
            'fields': ('services',),
            'description': 'Отметьте услуги, которые выполняет этот специалист.',
        }),
    )
    filter_horizontal = ('services',)

    class Media:
        css = {'all': ('admin/css/schedule_widget.css',)}
        js  = ('admin/js/specialist_admin.js',)

    # ── Кастомные URL (AJAX-эндпоинты внутри admin) ───────────────────

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                '<int:pk>/portfolio-action/',
                self.admin_site.admin_view(self.portfolio_action_view),
                name='specialists_specialist_portfolio_action',
            ),
        ]
        return custom + urls

    def portfolio_action_view(self, request, pk):
        """
        AJAX: применяет решение владельца о судьбе портфолио.
        POST { action: 'hide' | 'keep' }
        """
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        try:
            specialist = Specialist.objects.get(pk=pk)
        except Specialist.DoesNotExist:
            return JsonResponse({'error': 'Специалист не найден'}, status=404)

        action = request.POST.get('action')
        if action == 'hide':
            count = PortfolioWork.objects.filter(
                specialist=specialist, is_visible=True
            ).update(is_visible=False)
            logger.info(
                'Пользователь %s скрыл %d работ портфолио специалиста pk=%s',
                request.user, count, pk,
            )
            return JsonResponse({'ok': True, 'hidden': count})
        elif action == 'keep':
            logger.info(
                'Пользователь %s оставил портфолио специалиста pk=%s видимым',
                request.user, pk,
            )
            return JsonResponse({'ok': True, 'hidden': 0})
        elif action == 'show':
            count = PortfolioWork.objects.filter(
                specialist=specialist, is_visible=False
            ).update(is_visible=True)
            logger.info(
                'Пользователь %s показал %d работ портфолио специалиста pk=%s',
                request.user, count, pk,
            )
            return JsonResponse({'ok': True, 'shown': count})
        else:
            return JsonResponse({'error': 'Неизвестное действие'}, status=400)

    # ── change_view: добавляем блок управления портфолио ──────────────

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        try:
            specialist = Specialist.objects.get(pk=object_id)
            visible_count = PortfolioWork.objects.filter(
                specialist=specialist, is_visible=True
            ).count()
            hidden_count = PortfolioWork.objects.filter(
                specialist=specialist, is_visible=False
            ).count()
            extra_context['portfolio_visible'] = visible_count
            extra_context['portfolio_hidden']  = hidden_count
            extra_context['specialist_pk']     = specialist.pk
            extra_context['specialist_active'] = specialist.is_active
        except Specialist.DoesNotExist:
            pass
        return super().change_view(request, object_id, form_url, extra_context)

    # ── Колонки списка ────────────────────────────────────────────────

    def portfolio_count(self, obj):
        visible = PortfolioWork.objects.filter(specialist=obj, is_visible=True).count()
        total   = PortfolioWork.objects.filter(specialist=obj).count()
        return f'{visible} / {total}'
    portfolio_count.short_description = 'Работ (видно/всего)'

    def schedule_summary(self, obj):
        day_labels = {0:'Пн',1:'Вт',2:'Ср',3:'Чт',4:'Пт',5:'Сб',6:'Вс'}
        days = obj.work_days.values_list('weekday', flat=True).order_by('weekday')
        return ' '.join(day_labels[d] for d in days) if days else '—'
    schedule_summary.short_description = 'Рабочие дни'

    # ── Действия ─────────────────────────────────────────────────────

    @admin.action(description='Скрыть все работы с сайта')
    def hide_portfolio(self, request, queryset):
        for sp in queryset:
            PortfolioWork.objects.filter(specialist=sp, is_visible=True).update(is_visible=False)
        self.message_user(request, 'Работы скрыты с публичного сайта', messages.SUCCESS)

    @admin.action(description='Показать все работы на сайте')
    def show_portfolio(self, request, queryset):
        for sp in queryset:
            PortfolioWork.objects.filter(specialist=sp, is_visible=False).update(is_visible=True)
        self.message_user(request, 'Работы снова видны на сайте', messages.SUCCESS)


# ── Остальные admin-классы ────────────────────────────────────────────

@admin.register(SpecialistScheduleException)
class ScheduleExceptionAdmin(admin.ModelAdmin):
    form           = ScheduleExceptionInlineForm
    list_display   = ('date', 'specialist', 'time_start', 'time_end', 'comment')
    list_filter    = ('specialist',)
    date_hierarchy = 'date'
    ordering       = ('date',)


@admin.register(SpecialistDocument)
class SpecialistDocumentAdmin(admin.ModelAdmin):
    list_display = ('specialist', 'title', 'uploaded_at')
    list_filter  = ('specialist',)