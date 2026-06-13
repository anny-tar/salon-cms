import logging
from django.db import models
from django.urls import reverse
from specialists.models import Specialist
from services.models import ServiceCategory
from appointments.models import Appointment
from config.seo_mixin import SeoMixin
from config.utils import ru_slugify

logger = logging.getLogger(__name__)


class PhotoConsent(models.Model):
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE,
        verbose_name='Запись', related_name='photo_consent',
    )
    scan        = models.FileField('Скан согласия', upload_to='consents/')
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Согласие на фото'
        verbose_name_plural = 'Согласия на фото'

    def __str__(self):
        return f'Согласие — {self.appointment}'


class PortfolioWork(SeoMixin, models.Model):
    SOURCE_APPOINTMENT = 'appointment'
    SOURCE_DIRECT      = 'direct'
    SOURCE_CHOICES = [
        (SOURCE_APPOINTMENT, 'Из визита'),
        (SOURCE_DIRECT,      'Прямая загрузка'),
    ]

    specialist        = models.ForeignKey(
        Specialist, on_delete=models.PROTECT,
        verbose_name='Специалист', db_index=True,
    )
    service_category  = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Категория услуги',
    )
    appointment = models.ForeignKey(
        Appointment, on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name='Визит',
    )
    source = models.CharField(
        'Источник', max_length=20,
        choices=SOURCE_CHOICES, default=SOURCE_APPOINTMENT,
    )
    photo_original    = models.ImageField('Оригинал фото', upload_to='portfolio/original/')
    photo_watermarked = models.ImageField(
        'Фото с водяным знаком', upload_to='portfolio/watermarked/', blank=True,
    )
    specialist_liability = models.BooleanField('Специалист принял ответственность', default=False)
    liability_datetime   = models.DateTimeField('Дата принятия ответственности', null=True, blank=True)
    work_date  = models.DateField('Дата работы')
    is_visible = models.BooleanField('Видно на сайте', default=True, db_index=True)
    created_at = models.DateTimeField('Добавлено', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Изменено', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Работа в портфолио'
        verbose_name_plural = 'Работы в портфолио'
        ordering = ['-work_date']

    def __str__(self):
        return f'{self.specialist} — {self.work_date}'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = ru_slugify(f'{self.specialist.full_name}-{self.work_date}')
            self.slug = self._make_unique_slug(base)
        super().save(*args, **kwargs)

    def _make_unique_slug(self, base):
        slug, counter = base, 1
        while PortfolioWork.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f'{base}-{counter}'
            counter += 1
        return slug

    def get_absolute_url(self):
        return reverse('public:portfolio_detail', kwargs={'slug': self.slug})