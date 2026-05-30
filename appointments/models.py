from django.db import models
from datetime import datetime, timedelta
from clients.models import Client
from specialists.models import Specialist
from services.models import Service


class Appointment(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_NO_SHOW = 'no_show'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Ожидает подтверждения'),
        (STATUS_CONFIRMED, 'Подтверждена'),
        (STATUS_IN_PROGRESS, 'В процессе'),
        (STATUS_COMPLETED, 'Завершена'),
        (STATUS_NO_SHOW, 'Не явился'),
        (STATUS_CANCELLED, 'Отменена'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        verbose_name='Клиент',
    )
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        verbose_name='Специалист',
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        verbose_name='Услуга',
    )
    date = models.DateField('Дата', db_index=True)
    time_start = models.TimeField('Начало')
    time_end = models.TimeField('Конец', blank=True)
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True,
    )
    reference_photo = models.ImageField(
        'Референс клиента',
        upload_to='references/',
        null=True,
        blank=True,
    )
    comment = models.TextField('Комментарий', blank=True)
    pd_consent_datetime = models.DateTimeField(
        'Дата согласия на обработку ПД',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['date', 'time_start']

    def __str__(self):
        return f'{self.date} {self.time_start} — {self.client} ({self.specialist})'

    def save(self, *args, **kwargs):
        # Автоматически вычисляем время окончания из длительности услуги
        if self.time_start and self.service_id:
            start_dt = datetime.combine(datetime.today(), self.time_start)
            end_dt = start_dt + timedelta(minutes=self.service.duration)
            self.time_end = end_dt.time()
        super().save(*args, **kwargs)