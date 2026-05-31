from django.db import models
from django.contrib.auth.models import User


class Specialist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользователь',
        null=True,
        blank=True,
    )
    full_name = models.CharField('ФИО', max_length=255)
    specialization = models.CharField('Специализация', max_length=255)
    photo = models.ImageField('Фото', upload_to='specialists/', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)

    # Рабочее расписание: {"mon": ["09:00", "20:00"], "tue": [...], ...}
    work_schedule = models.JSONField(
        'Рабочее расписание',
        default=dict,
        blank=True,
        help_text='Формат: {"mon": ["09:00","20:00"], "tue": ["09:00","20:00"]}'
    )

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class SpecialistDocument(models.Model):
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Специалист',
    )
    title = models.CharField('Название документа', max_length=255)
    file = models.FileField('Файл', upload_to='specialist_docs/')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Документ специалиста'
        verbose_name_plural = 'Документы специалиста'

    def __str__(self):
        return f'{self.specialist.full_name} — {self.title}'