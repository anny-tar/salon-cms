from django.db import models


class Post(models.Model):
    TYPE_NEWS = 'news'
    TYPE_PROMO = 'promo'

    TYPE_CHOICES = [
        (TYPE_NEWS, 'Новость'),
        (TYPE_PROMO, 'Акция'),
    ]

    title = models.CharField('Заголовок', max_length=255)
    body = models.TextField('Текст')
    photo = models.ImageField('Фото', upload_to='news/', null=True, blank=True)
    post_type = models.CharField(
        'Тип',
        max_length=10,
        choices=TYPE_CHOICES,
        default=TYPE_NEWS,
    )
    is_published = models.BooleanField('Опубликовано', default=False)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Новости и акции'
        ordering = ['-created_at']

    def __str__(self):
        return self.title