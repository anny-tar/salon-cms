from django.db import models

FONT_CHOICES = [
    ('Roboto', 'Roboto'),
    ('Open Sans', 'Open Sans'),
    ('Montserrat', 'Montserrat'),
    ('Lato', 'Lato'),
    ('Raleway', 'Raleway'),
    ('Nunito', 'Nunito'),
    ('Playfair Display', 'Playfair Display'),
    ('Merriweather', 'Merriweather'),
    ('PT Sans', 'PT Sans'),
    ('Ubuntu', 'Ubuntu'),
]


class SiteSettings(models.Model):
    # Основное
    salon_name = models.CharField('Название салона', max_length=255, default='Мой салон')
    logo = models.ImageField('Логотип', upload_to='branding/', null=True, blank=True)
    favicon = models.ImageField('Фавиконка', upload_to='branding/', null=True, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адрес', max_length=255, blank=True)

    # Брендинг
    color_primary = models.CharField('Основной цвет', max_length=7, default='#4F81BD')
    color_secondary = models.CharField('Вторичный цвет', max_length=7, default='#2E4057')
    color_accent = models.CharField('Акцентный цвет', max_length=7, default='#F6AE2D')
    color_background = models.CharField('Фон', max_length=7, default='#FFFFFF')
    font = models.CharField('Шрифт', max_length=100, choices=FONT_CHOICES, default='Roboto')

    # Документы
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
    watermark_text = models.CharField('Текст водяного знака', max_length=100, blank=True)
    watermark_opacity = models.FloatField('Прозрачность (0.1 — 1.0)', default=0.3)

    # Баннер (секция 1, ручной ввод)
    banner_title = models.CharField('Баннер: заголовок', max_length=255, blank=True)
    banner_subtitle = models.CharField('Баннер: подзаголовок', max_length=255, blank=True)
    banner_image = models.ImageField('Баннер: фоновое фото', upload_to='branding/', null=True, blank=True)
    banner_cta_text = models.CharField('Баннер: текст кнопки', max_length=100, blank=True, default='Записаться')

    # Текст + Изображение (секция 6, ручной ввод)
    text_image_title = models.CharField('Блок текст+фото: заголовок', max_length=255, blank=True)
    text_image_body = models.TextField('Блок текст+фото: текст', blank=True)
    text_image_photo = models.ImageField('Блок текст+фото: фото', upload_to='branding/', null=True, blank=True)

    # Шаги (секция 8, ручной ввод) — хранятся в JSON
    steps_title = models.CharField('Шаги: заголовок', max_length=255, blank=True, default='Как это работает')
    steps_config = models.JSONField(
        'Шаги: список',
        default=list,
        blank=True,
        help_text='Пример: [{"title": "Запись", "text": "Выберите услугу онлайн"}]'
    )

    # Таблица (секция 9, ручной ввод)
    table_title = models.CharField('Таблица: заголовок', max_length=255, blank=True)
    table_config = models.JSONField(
        'Таблица: данные',
        default=dict,
        blank=True,
        help_text='Пример: {"headers": ["Услуга","Цена"], "rows": [["Маникюр","2500"]]}'
    )

    # Конструктор секций
    sections_config = models.JSONField(
        'Конфигурация секций',
        default=list,
        blank=True,
        help_text='Порядок и видимость секций главной страницы'
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.salon_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj