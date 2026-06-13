"""
SEO-миксин для моделей с публичными страницами-карточками.
Подключается через множественное наследование.
"""
from django.db import models
from django.utils.text import slugify


class SeoMixin(models.Model):
    """
    Добавляет SEO-поля на модель:
    slug, seo_title, meta_description, h1, alt_text.
    """
    slug = models.SlugField(
        'URL (slug)',
        max_length=200,
        unique=True,
        blank=True,
        help_text='Заполняется автоматически. Можно изменить вручную.',
        allow_unicode=False,
    )
    seo_title = models.CharField(
        'SEO заголовок (title)',
        max_length=255,
        blank=True,
        help_text='Если не заполнен — используется название.',
    )
    meta_description = models.TextField(
        'Meta description',
        max_length=300,
        blank=True,
    )
    h1 = models.CharField(
        'Заголовок страницы (H1)',
        max_length=255,
        blank=True,
        help_text='Если не заполнен — используется название.',
    )
    alt_text = models.CharField(
        'Alt для главного изображения',
        max_length=255,
        blank=True,
    )

    class Meta:
        abstract = True

    def get_seo_title(self, fallback: str = '') -> str:
        return self.seo_title or fallback

    def get_h1(self, fallback: str = '') -> str:
        return self.h1 or fallback