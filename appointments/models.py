from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from clients.models import Client
from specialists.models import Specialist
from services.models import Service


class Appointment(models.Model):

    STATUS_PENDING    = 'pending'
    STATUS_CONFIRMED  = 'confirmed'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED  = 'completed'
    STATUS_NO_SHOW    = 'no_show'
    STATUS_CANCELLED  = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING,    'Ожидает подтверждения'),
        (STATUS_CONFIRMED,  'Подтверждена'),
        (STATUS_IN_PROGRESS,'В процессе'),
        (STATUS_COMPLETED,  'Завершена'),
        (STATUS_NO_SHOW,    'Не явился'),
        (STATUS_CANCELLED,  'Отменена'),
    ]

    client     = models.ForeignKey(Client,     on_delete=models.PROTECT, verbose_name='Клиент')
    specialist = models.ForeignKey(Specialist, on_delete=models.PROTECT, verbose_name='Специалист')
    service    = models.ForeignKey(Service,    on_delete=models.PROTECT, verbose_name='Услуга')

    date       = models.DateField('Дата', db_index=True)
    time_start = models.TimeField('Начало')
    time_end   = models.TimeField('Конец', blank=True)  # вычисляется в clean()

    status = models.CharField(
        'Статус', max_length=20,
        choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True,
    )
    comment = models.TextField('Комментарий', blank=True)
    pd_consent_datetime = models.DateTimeField(
        'Дата согласия на обработку ПД', null=True, blank=True,
    )
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Изменена', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['date', 'time_start']

    def __str__(self):
        return f'{self.date} {self.time_start} — {self.client} ({self.specialist})'

    def clean(self):
        """Вычисляем time_end на этапе валидации, не в save()."""
        if self.time_start and self.service_id:
            start_dt = datetime.combine(datetime.today(), self.time_start)
            end_dt   = start_dt + timedelta(minutes=self.service.duration)
            self.time_end = end_dt.time()

    def save(self, *args, **kwargs):
        # Гарантируем что time_end всегда заполнен,
        # даже если вызов идёт в обход full_clean()
        if self.time_start and self.service_id and not self.time_end:
            start_dt  = datetime.combine(datetime.today(), self.time_start)
            self.time_end = (start_dt + timedelta(minutes=self.service.duration)).time()
        super().save(*args, **kwargs)


class AppointmentReferencePhoto(models.Model):
    """Фото-референсы клиента к записи. Любое количество."""
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE,
        related_name='reference_photos', verbose_name='Запись',
    )
    photo      = models.ImageField('Фото', upload_to='references/')
    uploaded_at = models.DateTimeField('Загружено', auto_now_add=True)

    class Meta:
        verbose_name = 'Референс'
        verbose_name_plural = 'Референсы клиента'

    def __str__(self):
        return f'Референс к {self.appointment}'