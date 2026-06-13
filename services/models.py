from django.db import models
from django.urls import reverse
from config.seo_mixin import SeoMixin
from config.utils import ru_slugify


class ServiceCategory(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(SeoMixin, models.Model):
    name        = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    category    = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Категория',
    )
    duration  = models.PositiveIntegerField('Длительность (мин.)')
    price     = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_unique_slug(ru_slugify(self.name))
        super().save(*args, **kwargs)

    def _make_unique_slug(self, base):
        slug, counter = base, 1
        while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse('public:service_detail', kwargs={'slug': self.slug})