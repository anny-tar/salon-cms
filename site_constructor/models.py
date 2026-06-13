from django.db import models
from ordered_model.models import OrderedModel

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
    salon_name  = models.CharField('Название салона', max_length=255, default='Мой салон')
    logo        = models.ImageField('Логотип', upload_to='branding/', null=True, blank=True)
    favicon     = models.ImageField('Фавиконка', upload_to='branding/', null=True, blank=True)
    phone       = models.CharField('Телефон', max_length=20, blank=True)
    email       = models.EmailField('Email', blank=True)
    address     = models.CharField('Адрес', max_length=255, blank=True)

    color_primary    = models.CharField('Основной цвет', max_length=7, default='#4F81BD')
    color_secondary  = models.CharField('Вторичный цвет', max_length=7, default='#2E4057')
    color_accent     = models.CharField('Акцентный цвет', max_length=7, default='#F6AE2D')
    color_background = models.CharField('Фон', max_length=7, default='#FFFFFF')
    font = models.CharField('Шрифт', max_length=100, choices=FONT_CHOICES, default='Roboto')

    privacy_policy = models.FileField(
        'Политика конфиденциальности (PDF)',
        upload_to='documents/', null=True, blank=True,
    )

    WATERMARK_LOGO = 'logo'
    WATERMARK_TEXT = 'text'
    WATERMARK_CHOICES = [
        (WATERMARK_LOGO, 'Логотип'),
        (WATERMARK_TEXT, 'Текст'),
    ]
    watermark_type    = models.CharField('Тип водяного знака', max_length=10,
                                          choices=WATERMARK_CHOICES, default=WATERMARK_TEXT)
    watermark_text    = models.CharField('Текст водяного знака', max_length=100, blank=True)
    watermark_opacity = models.FloatField('Прозрачность (0.1 — 1.0)', default=0.3)

    # SEO главной страницы
    seo_title        = models.CharField('SEO заголовок (title)', max_length=255, blank=True)
    meta_description = models.TextField('Meta description', max_length=300, blank=True)
    robots           = models.CharField(
        'Robots', max_length=50, default='index, follow',
        help_text='Например: index, follow или noindex, nofollow',
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


class SitePage(OrderedModel):
    """
    Страницы публичного сайта с настройкой порядка, видимости и SEO.
    Фиксированный набор — 5 страниц, создаётся через data migration.
    """

    PAGE_SERVICES  = 'services'
    PAGE_TEAM      = 'team'
    PAGE_PORTFOLIO = 'portfolio'
    PAGE_NEWS      = 'news'
    PAGE_PRODUCTS  = 'products'

    PAGE_CHOICES = [
        (PAGE_SERVICES,  'Услуги'),
        (PAGE_TEAM,      'Команда'),
        (PAGE_PORTFOLIO, 'Портфолио'),
        (PAGE_NEWS,      'Новости и акции'),
        (PAGE_PRODUCTS,  'Товары'),
    ]

    PAGE_DEFAULTS = {
        PAGE_SERVICES:  {'nav_label': 'Услуги',          'slug': 'services',  'order': 0},
        PAGE_TEAM:      {'nav_label': 'Команда',         'slug': 'team',      'order': 1},
        PAGE_PORTFOLIO: {'nav_label': 'Портфолио',       'slug': 'portfolio', 'order': 2},
        PAGE_NEWS:      {'nav_label': 'Новости и акции', 'slug': 'news',      'order': 3},
        PAGE_PRODUCTS:  {'nav_label': 'Товары',          'slug': 'products',  'order': 4},
    }

    page_type        = models.CharField('Тип страницы', max_length=20, choices=PAGE_CHOICES, unique=True)
    nav_label        = models.CharField('Название в навигации', max_length=100)
    slug             = models.SlugField('Slug (URL)', max_length=100, unique=True)
    is_visible       = models.BooleanField('Видна в навигации', default=True)
    seo_title        = models.CharField('SEO title', max_length=255, blank=True)
    meta_description = models.TextField('Meta description', max_length=300, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = 'Страница сайта'
        verbose_name_plural = 'Страницы сайта'

    def __str__(self):
        return self.nav_label

    def get_url(self):
        return f'/{self.slug}/'

    @classmethod
    def ensure_defaults(cls):
        """Создаёт страницы по умолчанию если их нет."""
        for page_type, defaults in cls.PAGE_DEFAULTS.items():
            cls.objects.get_or_create(
                page_type=page_type,
                defaults={**defaults, 'is_visible': True},
            )


class Section(OrderedModel):

    TYPE_BANNER   = 'banner'
    TYPE_SERVICES = 'services'
    TYPE_TEAM     = 'team'
    TYPE_PORTFOLIO= 'portfolio'
    TYPE_NEWS     = 'news'
    TYPE_PRODUCTS = 'products'
    TYPE_TEXT_IMG = 'text_image'
    TYPE_STEPS    = 'steps'
    TYPE_CONTACTS = 'contacts'
    TYPE_MAP      = 'map'

    TYPE_CHOICES = [
        (TYPE_BANNER,    'Баннер'),
        (TYPE_SERVICES,  'Услуги'),
        (TYPE_TEAM,      'О команде'),
        (TYPE_PORTFOLIO, 'Портфолио'),
        (TYPE_NEWS,      'Новости и акции'),
        (TYPE_PRODUCTS,  'Товары'),
        (TYPE_TEXT_IMG,  'Текст + Изображение'),
        (TYPE_STEPS,     'Шаги'),
        (TYPE_CONTACTS,  'Контакты и форма'),
        (TYPE_MAP,       'Карта'),
    ]

    TYPE_ICONS = {
        TYPE_BANNER:    '🖼',
        TYPE_SERVICES:  '✂️',
        TYPE_TEAM:      '👥',
        TYPE_PORTFOLIO: '📸',
        TYPE_NEWS:      '📰',
        TYPE_PRODUCTS:  '🛍',
        TYPE_TEXT_IMG:  '📝',
        TYPE_STEPS:     '📋',
        TYPE_CONTACTS:  '📞',
        TYPE_MAP:       '🗺',
    }

    site = models.ForeignKey(
        SiteSettings, on_delete=models.CASCADE,
        related_name='sections', verbose_name='Сайт',
    )
    type       = models.CharField('Тип секции', max_length=20, choices=TYPE_CHOICES)
    settings   = models.JSONField('Настройки', default=dict, blank=True)
    image      = models.ImageField(
        'Изображение', upload_to='sections/', null=True, blank=True,
        help_text='Используется в секциях «Баннер» и «Текст + Изображение»',
    )
    is_visible = models.BooleanField('Видна на сайте', default=True)
    anchor     = models.SlugField(
        'Якорь (anchor)', max_length=100, blank=True,
        help_text='Например: services, team, booking. Используется в навигации.',
    )

    order_with_respect_to = 'site'

    class Meta(OrderedModel.Meta):
        verbose_name = 'Секция'
        verbose_name_plural = 'Секции'

    def __str__(self):
        icon = self.TYPE_ICONS.get(self.type, '')
        return f'{icon} {self.get_type_display()}'

    @property
    def icon(self):
        return self.TYPE_ICONS.get(self.type, '')


class SectionStep(models.Model):
    """Шаг в секции «Шаги». Редактируется через inline в admin."""
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE,
        related_name='steps', verbose_name='Секция',
    )
    number  = models.CharField('Номер/символ', max_length=10,
                               help_text='Например: 01, 1, A, ★')
    text    = models.TextField('Текст шага')
    order   = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Шаг'
        verbose_name_plural = 'Шаги'
        ordering = ['order']

    def __str__(self):
        return f'{self.number}. {self.text[:50]}'