from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Specialist
from portfolio.models import PortfolioWork


@receiver(pre_save, sender=Specialist)
def handle_specialist_deactivation(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = Specialist.objects.get(pk=instance.pk)
    except Specialist.DoesNotExist:
        return

    # Специалист был активен, а теперь деактивируется
    if old.is_active and not instance.is_active:
        # Скрываем все его работы с публичного сайта
        PortfolioWork.objects.filter(
            specialist=instance,
            is_visible=True,
        ).update(is_visible=False)