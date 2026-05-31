from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from appointments.models import Appointment
from clients.models import Client
from specialists.models import Specialist
from services.models import Service, ServiceCategory
from portfolio.models import PortfolioWork, PhotoConsent
from products.models import Product
from news.models import Post
from site_constructor.models import SiteSettings


class Command(BaseCommand):
    help = 'Создаёт группы и права доступа'

    def handle(self, *args, **kwargs):
        # Удаляем старые группы если есть
        Group.objects.filter(name__in=['Владелец', 'Администратор', 'Специалист']).delete()

        # --- Специалист ---
        specialist_group = Group.objects.create(name='Специалист')
        # Специалист не имеет доступа к админке — только к своему интерфейсу

        # --- Администратор ---
        admin_group = Group.objects.create(name='Администратор')
        admin_permissions = []

        # Клиенты — полный доступ
        ct = ContentType.objects.get_for_model(Client)
        admin_permissions += list(Permission.objects.filter(content_type=ct))

        # Записи — полный доступ
        ct = ContentType.objects.get_for_model(Appointment)
        admin_permissions += list(Permission.objects.filter(content_type=ct))

        # Специалисты — только просмотр
        ct = ContentType.objects.get_for_model(Specialist)
        admin_permissions += list(Permission.objects.filter(content_type=ct, codename__startswith='view'))

        # Услуги — только просмотр
        ct = ContentType.objects.get_for_model(Service)
        admin_permissions += list(Permission.objects.filter(content_type=ct, codename__startswith='view'))

        # Портфолио — загрузка согласий
        ct = ContentType.objects.get_for_model(PhotoConsent)
        admin_permissions += list(Permission.objects.filter(content_type=ct))

        # Работы портфолио — только просмотр
        ct = ContentType.objects.get_for_model(PortfolioWork)
        admin_permissions += list(Permission.objects.filter(content_type=ct, codename__startswith='view'))

        admin_group.permissions.set(admin_permissions)

        # --- Владелец ---
        owner_group = Group.objects.create(name='Владелец')
        # Владелец получает все права
        all_permissions = Permission.objects.all()
        owner_group.permissions.set(all_permissions)

        self.stdout.write(self.style.SUCCESS('Группы успешно созданы: Владелец, Администратор, Специалист'))