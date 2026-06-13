"""
Формы для каждого типа секции.
settings JSONField сериализуется/десериализуется через методы формы.
"""
from django import forms


# ── Базовая форма ─────────────────────────────────────────────────────

class BaseSectionForm(forms.Form):
    """
    Базовый класс. Дочерние классы определяют поля.
    Метод to_settings() возвращает словарь для сохранения в Section.settings.
    Метод from_settings() заполняет initial из Section.settings.
    """

    @classmethod
    def from_settings(cls, settings: dict):
        return cls(initial=settings)

    def to_settings(self) -> dict:
        return self.cleaned_data


# ── Общие поля (присутствуют во всех секциях) ────────────────────────

class CommonFieldsMixin:
    pass  # заголовок и подзаголовок добавлены в каждую форму явно


# ── Баннер ────────────────────────────────────────────────────────────

ALIGN_CHOICES = [
    ('center', 'По центру'),
    ('left',   'По левому краю'),
    ('right',  'По правому краю'),
]

OVERLAY_CHOICES = [
    ('dark',  'Затемнение'),
    ('light', 'Осветление'),
    ('none',  'Без маски'),
]


class BannerSectionForm(BaseSectionForm):
    title     = forms.CharField(label='Заголовок', max_length=255, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Добро пожаловать'}))
    subtitle  = forms.CharField(label='Подзаголовок', max_length=255, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Краткое описание'}))
    cta_text  = forms.CharField(label='Текст кнопки', max_length=100, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Записаться'}))
    align     = forms.ChoiceField(label='Выравнивание', choices=ALIGN_CHOICES, initial='center')
    overlay   = forms.ChoiceField(label='Маска фона', choices=OVERLAY_CHOICES, initial='dark')


# ── Живые секции (общая форма для services/team/portfolio/news) ───────

COUNT_CHOICES = [(str(n), str(n)) for n in [3, 4, 6, 8, 9, 12]] + [('all', 'Все')]
DISPLAY_CHOICES = [('grid', 'Сетка'), ('list', 'Список')]


class LiveSectionForm(BaseSectionForm):
    title       = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle    = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 3}))
    count       = forms.ChoiceField(label='Количество', choices=COUNT_CHOICES, initial='6')
    display     = forms.ChoiceField(label='Отображение', choices=DISPLAY_CHOICES, initial='grid')


class ProductsSectionForm(BaseSectionForm):
    """Товары — без поля количества."""
    title       = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle    = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 3}))
    display     = forms.ChoiceField(label='Отображение', choices=DISPLAY_CHOICES, initial='grid')


# ── Текст + Изображение ───────────────────────────────────────────────

LAYOUT_CHOICES = [
    ('img_right',  'Текст слева, фото справа'),
    ('img_left',   'Фото слева, текст справа'),
    ('img_bottom', 'Текст сверху, фото снизу'),
]


class TextImageSectionForm(BaseSectionForm):
    title    = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    body     = forms.CharField(label='Текст', required=False,
                               widget=forms.Textarea(attrs={'rows': 5}))
    layout   = forms.ChoiceField(label='Расположение', choices=LAYOUT_CHOICES, initial='img_right')


# ── Шаги ─────────────────────────────────────────────────────────────
# Шаги хранятся в JSON как список: [{"number": "01", "text": "..."}, ...]
# Форма содержит только заголовок/подзаголовок/описание.
# Сами шаги редактируются через отдельный inline в admin.

class StepsSectionForm(BaseSectionForm):
    title       = forms.CharField(label='Заголовок блока', max_length=255, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Как это работает'}))
    subtitle    = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 3}))


# ── Контакты и форма ──────────────────────────────────────────────────

SIDE_CHOICES = [
    ('left',  'Слева'),
    ('right', 'Справа'),
    ('none',  'Не показывать'),
]


class ContactsSectionForm(BaseSectionForm):
    title    = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle = forms.CharField(label='Подзаголовок', max_length=255, required=False)

    contacts_side = forms.ChoiceField(
        label='Расположение контактов', choices=SIDE_CHOICES, initial='left'
    )
    phone     = forms.CharField(label='Телефон', max_length=50, required=False)
    email     = forms.EmailField(label='Email', required=False)
    vk        = forms.URLField(label='ВКонтакте', required=False,
                               widget=forms.URLInput(attrs={'placeholder': 'https://vk.com/...'}))
    telegram  = forms.CharField(label='Telegram', max_length=100, required=False,
                                widget=forms.TextInput(attrs={'placeholder': '@username или ссылка'}))
    whatsapp  = forms.CharField(label='WhatsApp', max_length=50, required=False,
                                widget=forms.TextInput(attrs={'placeholder': '+7 900 000-00-00'}))
    instagram = forms.URLField(label='Instagram', required=False,
                               widget=forms.URLInput(attrs={'placeholder': 'https://instagram.com/...'}))

    form_side = forms.ChoiceField(
        label='Расположение формы записи', choices=SIDE_CHOICES, initial='right'
    )


# ── Карта ─────────────────────────────────────────────────────────────

class MapSectionForm(BaseSectionForm):
    title    = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    body     = forms.CharField(label='Текст', required=False,
                               widget=forms.Textarea(attrs={'rows': 3}))
    map_url  = forms.CharField(
        label='Ссылка для встраивания карты',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Вставьте iframe-ссылку из Яндекс Карт\n'
                           '(Поделиться → Встроить → скопируйте src из iframe)',
        }),
        help_text='Скопируйте значение атрибута src из кода встраивания Яндекс Карт',
    )


# ── Реестр форм по типу секции ────────────────────────────────────────

SECTION_FORM_MAP = {
    'banner':     BannerSectionForm,
    'services':   LiveSectionForm,
    'team':       LiveSectionForm,
    'portfolio':  LiveSectionForm,
    'news':       LiveSectionForm,
    'products':   ProductsSectionForm,
    'text_image': TextImageSectionForm,
    'steps':      StepsSectionForm,
    'contacts':   ContactsSectionForm,
    'map':        MapSectionForm,
}


def get_section_form(section_type: str, data=None, initial=None):
    """Возвращает нужную форму для типа секции."""
    form_class = SECTION_FORM_MAP.get(section_type)
    if not form_class:
        return None
    if data is not None:
        return form_class(data, initial=initial)
    return form_class(initial=initial)