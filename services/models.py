from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    duration = models.PositiveIntegerField('Длительность (мин.)')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return self.name