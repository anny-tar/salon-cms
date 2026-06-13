import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PortfolioWork

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PortfolioWork)
def apply_watermark_on_create(sender, instance, created, **kwargs):
    """Накладывает водяной знак после первого сохранения фото."""
    if not created:
        return
    if not instance.photo_original:
        return
    if instance.photo_watermarked:
        return

    try:
        from site_constructor.models import SiteSettings
        from .watermark import apply_watermark
        import os

        site = SiteSettings.get()
        watermarked = apply_watermark(instance.photo_original, site)
        filename = os.path.basename(instance.photo_original.name)

        # save=False чтобы не вызвать рекурсию через post_save
        instance.photo_watermarked.save(f'wm_{filename}', watermarked, save=False)
        # Обновляем только одно поле, не трогая updated_at остальных
        PortfolioWork.objects.filter(pk=instance.pk).update(
            photo_watermarked=instance.photo_watermarked.name
        )
    except Exception:
        logger.exception('Ошибка при наложении водяного знака на PortfolioWork pk=%s', instance.pk)