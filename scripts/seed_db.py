"""
Скрипт заполнения БД тестовыми данными.
Запуск: python manage.py shell < scripts/seed_db.py
"""
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta

print("=== Заполнение БД тестовыми данными ===")

# ── Суперпользователь ─────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@salon.ru', 'admin123')
    print("+ Суперпользователь: admin / admin123")
else:
    print("- Суперпользователь уже существует")

# ── Настройки сайта ───────────────────────────────────────────────────
from site_constructor.models import SiteSettings, Section

site, created = SiteSettings.objects.get_or_create(pk=1, defaults={
    'salon_name':        'Beauty Studio',
    'phone':             '+7 (900) 123-45-67',
    'email':             'info@beauty-studio.ru',
    'address':           'г. Москва, ул. Цветочная, д. 5',
    'color_primary':     '#4F81BD',
    'color_secondary':   '#2E4057',
    'color_accent':      '#F6AE2D',
    'color_background':  '#FFFFFF',
    'font':              'Montserrat',
    'watermark_type':    'text',
    'watermark_text':    'Beauty Studio',
    'watermark_opacity': 0.3,
    'show_services':     True,
    'show_team':         True,
    'show_portfolio':    True,
    'show_news':         True,
    'show_products':     True,
    'seo_title':         'Beauty Studio — салон красоты в Москве',
    'meta_description':  'Профессиональные услуги красоты: стрижки, окрашивание, маникюр. Запись онлайн.',
    'robots':            'index, follow',
})
print(f"{'+ Настройки сайта' if created else '- Настройки уже существуют'}")

# ── Категории и услуги ────────────────────────────────────────────────
from services.models import ServiceCategory, Service

cat_haircut,  _ = ServiceCategory.objects.get_or_create(name='Стрижки')
cat_color,    _ = ServiceCategory.objects.get_or_create(name='Окрашивание')
cat_manicure, _ = ServiceCategory.objects.get_or_create(name='Маникюр')
cat_care,     _ = ServiceCategory.objects.get_or_create(name='Уход за волосами')
print("+ Категории услуг")

services_data = [
    ('Стрижка мужская',        'Классическая мужская стрижка с укладкой.',           cat_haircut,   45,   800),
    ('Стрижка женская',        'Женская стрижка любой сложности.',                   cat_haircut,   60,  1500),
    ('Стрижка детская',        'Стрижка для детей до 12 лет.',                       cat_haircut,   30,   600),
    ('Окрашивание корней',     'Окрашивание отросших корней в тон основного цвета.',  cat_color,    90,  2500),
    ('Мелирование',            'Классическое или балаяж мелирование.',                cat_color,   120,  3500),
    ('Тонирование',            'Тонирование для насыщенности цвета.',                cat_color,    60,  1800),
    ('Маникюр классический',   'Классический маникюр с покрытием.',                  cat_manicure, 60,  1200),
    ('Маникюр аппаратный',     'Аппаратный маникюр без обрезания.',                  cat_manicure, 75,  1500),
    ('Восстановление волос',   'Кератиновое восстановление структуры волос.',         cat_care,    120,  4500),
    ('Маска для волос',        'Питательная маска с профессиональными средствами.',   cat_care,     45,   900),
]
for name, desc, cat, duration, price in services_data:
    Service.objects.get_or_create(name=name, defaults={
        'description': desc, 'category': cat,
        'duration': duration, 'price': price, 'is_active': True,
    })
print("+ Услуги (10 шт.)")

# ── Специалисты ───────────────────────────────────────────────────────
from specialists.models import Specialist, SpecialistWorkDay

specialists_data = [
    ('Иванова Мария Сергеевна',    'Парикмахер-стилист',   'Специализируется на женских стрижках и окрашивании. Опыт 8 лет.',   [0,1,2,3,4], '09:00', '18:00'),
    ('Петров Алексей Игоревич',    'Барбер',               'Мастер мужских стрижок и бритья. Чемпион городского конкурса.',     [1,2,3,4,5], '10:00', '19:00'),
    ('Сидорова Екатерина Павловна','Мастер маникюра',       'Опытный мастер маникюра и педикюра.',                              [0,2,3,4,5], '09:00', '17:00'),
    ('Козлова Анна Дмитриевна',    'Колорист',             'Специалист по окрашиванию и восстановлению волос. Стаж 5 лет.',     [0,1,3,4,6], '11:00', '20:00'),
]
for full_name, spec, desc, weekdays, t_start, t_end in specialists_data:
    obj, flag = Specialist.objects.get_or_create(full_name=full_name, defaults={
        'specialization': spec, 'description': desc, 'is_active': True,
    })
    if flag:
        for wd in weekdays:
            h_s, m_s = map(int, t_start.split(':'))
            h_e, m_e = map(int, t_end.split(':'))
            SpecialistWorkDay.objects.get_or_create(
                specialist=obj, weekday=wd,
                defaults={'time_start': time(h_s, m_s), 'time_end': time(h_e, m_e)},
            )

sv = {s.name: s for s in Service.objects.all()}
sp = {}
for s in Specialist.objects.all():
    sp[s.full_name.split()[0]] = s

sp['Иванова'].services.set([sv['Стрижка женская'], sv['Стрижка детская'], sv['Мелирование'], sv['Тонирование']])
sp['Петров'].services.set([sv['Стрижка мужская'], sv['Стрижка детская']])
sp['Сидорова'].services.set([sv['Маникюр классический'], sv['Маникюр аппаратный']])
sp['Козлова'].services.set([sv['Окрашивание корней'], sv['Мелирование'], sv['Тонирование'], sv['Восстановление волос'], sv['Маска для волос']])
print("+ Специалисты (4 шт.) с расписанием и услугами")

# ── Клиенты ───────────────────────────────────────────────────────────
from clients.models import Client, ClientTag

tag_vip,     _ = ClientTag.objects.get_or_create(name='VIP')
tag_regular, _ = ClientTag.objects.get_or_create(name='Постоянный')
tag_new,     _ = ClientTag.objects.get_or_create(name='Новый')

clients_data = [
    ('Смирнова Ольга Николаевна',  '+79001112233', [tag_vip, tag_regular]),
    ('Тихонова Валерия Андреевна', '+79002223344', [tag_regular]),
    ('Морозова Диана Викторовна',  '+79003334455', [tag_regular]),
    ('Зайцева Полина Максимовна',  '+79004445566', [tag_new]),
    ('Волков Дмитрий Сергеевич',   '+79005556677', [tag_regular]),
]
clients = []
for full_name, phone, tags in clients_data:
    c, _ = Client.objects.get_or_create(phone=phone, defaults={'full_name': full_name})
    c.tags.set(tags)
    clients.append(c)
print("+ Клиенты (5 шт.)")

# ── Записи ────────────────────────────────────────────────────────────
from appointments.models import Appointment

today = date.today()
appts = [
    (clients[0], sp['Иванова'],  sv['Стрижка женская'],     today,              time(10, 0), Appointment.STATUS_CONFIRMED),
    (clients[1], sp['Петров'],   sv['Стрижка мужская'],     today,              time(11, 0), Appointment.STATUS_CONFIRMED),
    (clients[2], sp['Сидорова'], sv['Маникюр классический'],today,              time(14, 0), Appointment.STATUS_PENDING),
    (clients[3], sp['Козлова'],  sv['Окрашивание корней'],   today+timedelta(1), time(12, 0), Appointment.STATUS_PENDING),
    (clients[4], sp['Петров'],   sv['Стрижка мужская'],     today+timedelta(2), time(15, 0), Appointment.STATUS_PENDING),
    (clients[0], sp['Козлова'],  sv['Мелирование'],          today-timedelta(7), time(11, 0), Appointment.STATUS_COMPLETED),
    (clients[1], sp['Иванова'],  sv['Стрижка женская'],      today-timedelta(5), time(10, 0), Appointment.STATUS_COMPLETED),
    (clients[2], sp['Сидорова'], sv['Маникюр аппаратный'],   today-timedelta(3), time(13, 0), Appointment.STATUS_COMPLETED),
]
for client, specialist, service, appt_date, appt_time, status in appts:
    Appointment.objects.get_or_create(
        client=client, specialist=specialist,
        service=service, date=appt_date, time_start=appt_time,
        defaults={'status': status, 'pd_consent_datetime': timezone.now()},
    )
print("+ Записи (8 шт.)")

# ── Новости ───────────────────────────────────────────────────────────
from news.models import Post

for title, body, post_type in [
    ('Скидка 20% на окрашивание в июне',
     'Весь июнь действует специальное предложение — скидка 20% на все виды окрашивания. Успейте записаться!',
     'promo'),
    ('Новый мастер маникюра в нашей команде',
     'Рады представить нового специалиста — Екатерину Сидорову. Специализируется на аппаратном маникюре.',
     'news'),
    ('Мы переехали в новый салон',
     'Уважаемые клиенты! Наш салон переехал по новому адресу: ул. Цветочная, д. 5. Ждём вас!',
     'news'),
]:
    Post.objects.get_or_create(title=title, defaults={
        'body': body, 'post_type': post_type, 'is_published': True,
    })
print("+ Новости (3 шт.)")

# ── Товары ────────────────────────────────────────────────────────────
from products.models import Product

for name, desc, price in [
    ('Шампунь Kerastase Bain Force',  'Восстанавливающий шампунь для повреждённых волос. 250 мл.', 1850),
    ('Маска Olaplex No.3',             'Домашнее средство для восстановления волос.',               2200),
    ('Масло Moroccanoil Treatment',    'Аргановое масло для блеска и питания волос. 100 мл.',       2500),
    ('Лак для ногтей OPI',             'Стойкий лак для ногтей. Коллекция 2024.',                    550),
]:
    Product.objects.get_or_create(name=name, defaults={
        'description': desc, 'price': price, 'is_active': True,
    })
print("+ Товары (4 шт.)")

# ── Секции главной страницы ───────────────────────────────────────────
if not Section.objects.filter(site=site).exists():
    for i, (sec_type, settings, anchor) in enumerate([
        ('banner',   {'title': 'Добро пожаловать в Beauty Studio', 'subtitle': 'Профессиональные услуги красоты в центре Москвы', 'cta_text': 'Записаться онлайн', 'cta_link': '#booking'}, 'top'),
        ('services', {'count': '6', 'display': 'grid'}, 'services'),
        ('team',     {'count': '4', 'display': 'grid'}, 'team'),
        ('portfolio',{'count': '6', 'display': 'grid'}, 'portfolio'),
        ('news',     {'count': '3', 'display': 'grid'}, 'news'),
        ('booking',  {'title': 'Запишитесь онлайн'},    'booking'),
    ]):
        Section.objects.create(
            site=site, type=sec_type, settings=settings,
            is_visible=True, order=i, anchor=anchor,
        )
    print("+ Секции главной страницы (6 шт.)")
else:
    print("- Секции уже существуют")

print("\n=== Готово! ===")
print("Вход: http://127.0.0.1:8000/admin/")
print("Логин: admin  |  Пароль: admin123")