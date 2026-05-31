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

    # Видимость страниц
    show_services = models.BooleanField('Показывать страницу Услуги', default=True)
    show_team = models.BooleanField('Показывать страницу Команда', default=True)
    show_portfolio = models.BooleanField('Показывать страницу Портфолио', default=True)
    show_news = models.BooleanField('Показывать страницу Новости', default=False)
    show_products = models.BooleanField('Показывать страницу Товары', default=False)

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
    
from django.db import models
from ordered_model.models import OrderedModel


class Section(OrderedModel):

    TYPE_BANNER = 'banner'
    TYPE_SERVICES = 'services'
    TYPE_TEAM = 'team'
    TYPE_PORTFOLIO = 'portfolio'
    TYPE_NEWS = 'news'
    TYPE_PRODUCTS = 'products'
    TYPE_TEXT_IMAGE = 'text_image'
    TYPE_STEPS = 'steps'
    TYPE_TABLE = 'table'
    TYPE_BOOKING = 'booking'

    TYPE_CHOICES = [
        (TYPE_BANNER,     'Баннер'),
        (TYPE_SERVICES,   'Услуги'),
        (TYPE_TEAM,       'О команде'),
        (TYPE_PORTFOLIO,  'Портфолио'),
        (TYPE_NEWS,       'Новости и акции'),
        (TYPE_PRODUCTS,   'Товары'),
        (TYPE_TEXT_IMAGE, 'Текст + Изображение'),
        (TYPE_STEPS,      'Шаги'),
        (TYPE_TABLE,      'Таблица'),
        (TYPE_BOOKING,    'Контакты и запись'),
    ]

    site = models.ForeignKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Сайт',
    )
    type = models.CharField('Тип секции', max_length=20, choices=TYPE_CHOICES)
    settings = models.JSONField('Настройки', default=dict, blank=True)

    order_with_respect_to = 'site'

    class Meta(OrderedModel.Meta):
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        return f'{self.get_type_display()} (позиция {self.order})'

    TYPE_BANNER = 'banner'
    TYPE_SERVICES = 'services'
    TYPE_TEAM = 'team'
    TYPE_PORTFOLIO = 'portfolio'
    TYPE_NEWS = 'news'
    TYPE_PRODUCTS = 'products'
    TYPE_TEXT_IMAGE = 'text_image'
    TYPE_STEPS = 'steps'
    TYPE_TABLE = 'table'
    TYPE_BOOKING = 'booking'

    TYPE_CHOICES = [
        (TYPE_BANNER,     'Баннер'),
        (TYPE_SERVICES,   'Услуги'),
        (TYPE_TEAM,       'О команде'),
        (TYPE_PORTFOLIO,  'Портфолио'),
        (TYPE_NEWS,       'Новости и акции'),
        (TYPE_PRODUCTS,   'Товары'),
        (TYPE_TEXT_IMAGE, 'Текст + Изображение'),
        (TYPE_STEPS,      'Шаги'),
        (TYPE_TABLE,      'Таблица'),
        (TYPE_BOOKING,    'Контакты и запись'),
    ]

    site = models.ForeignKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Сайт',
    )
    type = models.CharField('Тип секции', max_length=20, choices=TYPE_CHOICES)
    order = models.PositiveIntegerField('Порядок', default=0)
    settings = models.JSONField('Настройки', default=dict, blank=True)

    class Meta:
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'
        ordering = ['order']

    def __str__(self):
        return f'{self.get_type_display()} (позиция {self.order})'