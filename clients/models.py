from django.db import models


class Client(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    phone = models.CharField('Телефон', max_length=20, unique=True, db_index=True)
    email = models.EmailField('Email', blank=True)
    comment = models.TextField('Комментарий', blank=True)
    tags = models.CharField('Теги', max_length=255, blank=True, help_text='Через запятую')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.phone})'
    