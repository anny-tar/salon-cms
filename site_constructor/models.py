from django.db import models


class SiteSettings(models.Model):
    salon_name = models.CharField('Название салона', max_length=255, default='Мой салон')
    logo = models.ImageField('Логотип', upload_to='branding/', null=True, blank=True)
    favicon = models.ImageField('Фавиконка', upload_to='branding/', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    color_primary = models.CharField('Основной цвет', max_length=7, default='#4F81BD')
    color_secondary = models.CharField('Вторичный цвет', max_length=7, default='#2E4057')
    color_accent = models.CharField('Акцентный цвет', max_length=7, default='#F6AE2D')
    color_background = models.CharField('Фон', max_length=7, default='#FFFFFF')
    font = models.CharField('Шрифт', max_length=100, default='Roboto')
    privacy_policy = models.FileField(
        'Политика конфиденциальности (PDF)',
        upload_to='documents/',
        null=True,
        blank=True,
    )

    # Водяной знак
    WATERMARK_LOGO = 'logo'
    WATERMARK_TEXT = 'text'
    WATERMARK_CHOICES = [
        (WATERMARK_LOGO, 'Логотип'),
        (WATERMARK_TEXT, 'Текст'),
    ]
    watermark_type = models.CharField(
        'Тип водяного знака',
        max_length=10,
        choices=WATERMARK_CHOICES,
        default=WATERMARK_TEXT,
    )
    watermark_text = models.CharField(
        'Текст водяного знака',
        max_length=100,
        blank=True,
    )
    watermark_opacity = models.FloatField(
        'Прозрачность водяного знака',
        default=0.3,
    )

    # Конструктор секций — порядок и состав секций главной страницы
    sections_config = models.JSONField(
        'Конфигурация секций',
        default=list,
        blank=True,
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.salon_name

    def save(self, *args, **kwargs):
        # Singleton — всегда только одна запись
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj