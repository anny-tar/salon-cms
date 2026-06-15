from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными для защиты ВКР'

    def handle(self, *args, **options):
        exec(open('scripts/seed_vkr.py', encoding='utf-8').read())
        self.stdout.write(self.style.SUCCESS('Готово!'))