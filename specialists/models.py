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

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name