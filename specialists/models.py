import logging
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from config.seo_mixin import SeoMixin
from config.utils import ru_slugify

logger = logging.getLogger(__name__)


def validate_time_str(value):
    import re
    if value and not re.match(r"^\d{2}:\d{2}$", value):
        raise ValidationError(
            f"Введите время в формате ЧЧ:ММ, например 09:00. Получено: «{value}»"
        )


class Specialist(SeoMixin, models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT,
        verbose_name='Пользователь', null=True, blank=True,
    )
    full_name      = models.CharField('ФИО', max_length=255)
    specialization = models.CharField('Специализация', max_length=255)
    photo          = models.ImageField('Фото', upload_to='specialists/', null=True, blank=True)
    description    = models.TextField('Описание', blank=True)
    is_active      = models.BooleanField('Активен', default=True)
    services       = models.ManyToManyField(
        'services.Service', verbose_name='Услуги',
        blank=True, related_name='specialists',
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_unique_slug(ru_slugify(self.full_name))
        super().save(*args, **kwargs)

    def _make_unique_slug(self, base):
        slug = base
        counter = 1
        while Specialist.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse('public:specialist_detail', kwargs={'slug': self.slug})

    def get_hours_for_date(self, date):
        try:
            exc = self.schedule_exceptions.get(date=date)
            if exc.time_start is None:
                return None
            return (
                exc.time_start.strftime('%H:%M'),
                exc.time_end.strftime('%H:%M'),
            )
        except SpecialistScheduleException.DoesNotExist:
            pass
        try:
            day = self.work_days.get(weekday=date.weekday())
            return (
                day.time_start.strftime('%H:%M'),
                day.time_end.strftime('%H:%M'),
            )
        except SpecialistWorkDay.DoesNotExist:
            return None


class SpecialistWorkDay(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'),
        (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье'),
    ]
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE,
        related_name='work_days', verbose_name='Специалист',
    )
    weekday    = models.PositiveSmallIntegerField('День недели', choices=WEEKDAY_CHOICES)
    time_start = models.TimeField('Начало смены')
    time_end   = models.TimeField('Конец смены')

    class Meta:
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Базовое расписание'
        unique_together = [('specialist', 'weekday')]
        ordering = ['weekday']

    def __str__(self):
        return f'{self.get_weekday_display()}: {self.time_start.strftime("%H:%M")}–{self.time_end.strftime("%H:%M")}'

    def clean(self):
        if self.time_start and self.time_end and self.time_start >= self.time_end:
            raise ValidationError('Начало смены должно быть раньше конца.')


class SpecialistScheduleException(models.Model):
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE,
        related_name='schedule_exceptions', verbose_name='Специалист',
    )
    date       = models.DateField('Дата', db_index=True)
    time_start = models.TimeField('Начало работы', null=True, blank=True,
                                  help_text='Оставьте пустым для выходного дня')
    time_end   = models.TimeField('Конец работы', null=True, blank=True,
                                  help_text='Оставьте пустым для выходного дня')
    comment    = models.CharField('Комментарий', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Исключение в расписании'
        verbose_name_plural = 'Исключения в расписании'
        unique_together = [('specialist', 'date')]
        ordering = ['date']

    def __str__(self):
        if self.time_start is None:
            return f'{self.date} — выходной ({self.specialist.full_name})'
        return f'{self.date} {self.time_start.strftime("%H:%M")}–{self.time_end.strftime("%H:%M")} ({self.specialist.full_name})'

    @property
    def is_day_off(self):
        return self.time_start is None

    def clean(self):
        if self.time_start is not None and self.time_end is not None:
            if self.time_start >= self.time_end:
                raise ValidationError('Начало смены должно быть раньше конца.')
        if (self.time_start is None) != (self.time_end is None):
            raise ValidationError('Укажите оба поля или оставьте оба пустыми (выходной).')


class SpecialistDocument(models.Model):
    specialist  = models.ForeignKey(
        Specialist, on_delete=models.CASCADE,
        related_name='documents', verbose_name='Специалист',
    )
    title       = models.CharField('Название документа', max_length=255)
    file        = models.FileField('Файл', upload_to='specialist_docs/')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Документ специалиста'
        verbose_name_plural = 'Документы специалиста'

    def __str__(self):
        return f'{self.specialist.full_name} — {self.title}'