# Полный список доступных секций
# key — уникальный идентификатор
# label — название для админки
# type — live (живые данные) или manual (ручной ввод)

AVAILABLE_SECTIONS = [
    {'key': 'banner',    'label': 'Баннер',            'type': 'manual'},
    {'key': 'services',  'label': 'Услуги',             'type': 'live'},
    {'key': 'team',      'label': 'О команде',          'type': 'live'},
    {'key': 'portfolio', 'label': 'Портфолио',          'type': 'live'},
    {'key': 'news',      'label': 'Новости и акции',    'type': 'live'},
    {'key': 'products',  'label': 'Товары',             'type': 'live'},
    {'key': 'text_image','label': 'Текст + Изображение','type': 'manual'},
    {'key': 'steps',     'label': 'Шаги',               'type': 'manual'},
    {'key': 'table',     'label': 'Таблица',            'type': 'manual'},
    {'key': 'booking',   'label': 'Контакты и запись',  'type': 'live'},
]

DEFAULT_SECTIONS_CONFIG = [
    {'key': 'banner',    'enabled': True,  'order': 1},
    {'key': 'services',  'enabled': True,  'order': 2},
    {'key': 'team',      'enabled': True,  'order': 3},
    {'key': 'portfolio', 'enabled': True,  'order': 4},
    {'key': 'news',      'enabled': False, 'order': 5},
    {'key': 'products',  'enabled': False, 'order': 6},
    {'key': 'text_image','enabled': False, 'order': 7},
    {'key': 'steps',     'enabled': False, 'order': 8},
    {'key': 'table',     'enabled': False, 'order': 9},
    {'key': 'booking',   'enabled': True,  'order': 10},
]


def get_sections_config(site_settings):
    """Возвращает конфигурацию секций — из БД или дефолтную"""
    config = site_settings.sections_config
    if not config:
        return DEFAULT_SECTIONS_CONFIG
    return sorted(config, key=lambda s: s.get('order', 99))


def get_enabled_sections(site_settings):
    """Возвращает только включённые секции в нужном порядке"""
    return [s for s in get_sections_config(site_settings) if s.get('enabled')]