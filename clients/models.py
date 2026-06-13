from django.db import models


class ClientTag(models.Model):
    name = models.CharField('Тег', max_length=64, unique=True)

    class Meta:
        verbose_name = 'Тег клиента'
        verbose_name_plural = 'Теги клиентов'
        ordering = ['name']

    def __str__(self):
        return self.name


class Client(models.Model):
    full_name  = models.CharField('ФИО', max_length=255)
    phone      = models.CharField('Телефон', max_length=20, unique=True, db_index=True)
    email      = models.EmailField('Email', blank=True)
    comment    = models.TextField('Комментарий', blank=True)
    tags       = models.ManyToManyField(
        ClientTag, verbose_name='Теги',
        blank=True, related_name='clients',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Изменён', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.phone})'