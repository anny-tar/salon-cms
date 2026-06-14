from django.db import models
from django.urls import reverse
from config.seo_mixin import SeoMixin
from config.utils import ru_slugify


class Product(SeoMixin, models.Model):
    name        = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    price       = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    photo       = models.ImageField('Фото', upload_to='products/', null=True, blank=True)
    is_active   = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_unique_slug(ru_slugify(self.name))
        super().save(*args, **kwargs)

    def _make_unique_slug(self, base):
        slug, counter = base, 1
        while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse('public:product_detail', kwargs={'slug': self.slug})