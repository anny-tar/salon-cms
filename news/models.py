from django.db import models
from django.urls import reverse
from config.seo_mixin import SeoMixin
from config.utils import ru_slugify


class Post(SeoMixin, models.Model):
    TYPE_NEWS  = 'news'
    TYPE_PROMO = 'promo'
    TYPE_CHOICES = [
        (TYPE_NEWS,  'Новость'),
        (TYPE_PROMO, 'Акция'),
    ]

    title        = models.CharField('Заголовок', max_length=255)
    body         = models.TextField('Текст')
    photo        = models.ImageField('Фото', upload_to='news/', null=True, blank=True)
    post_type    = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES, default=TYPE_NEWS)
    is_published = models.BooleanField('Опубликовано', default=False)
    created_at   = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Новости и акции'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_unique_slug(ru_slugify(self.title))
        super().save(*args, **kwargs)

    def _make_unique_slug(self, base):
        slug, counter = base, 1
        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse('public:news_detail', kwargs={'slug': self.slug})