"""
Формы настроек для каждого типа секции.
Данные сохраняются в Section.settings (JSONField).
"""
from django import forms


class BannerSectionForm(forms.Form):
    title    = forms.CharField(label='Заголовок', max_length=255, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Добро пожаловать'}))
    subtitle = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    cta_text = forms.CharField(label='Текст кнопки', max_length=100, required=False,
                               widget=forms.TextInput(attrs={'placeholder': 'Записаться'}))
    align    = forms.ChoiceField(label='Выравнивание', choices=[
        ('center', 'По центру'), ('left', 'По левому краю'), ('right', 'По правому краю'),
    ])
    overlay  = forms.ChoiceField(label='Маска фона', choices=[
        ('dark', 'Затемнение'), ('light', 'Осветление'), ('none', 'Без маски'),
    ])


class LiveSectionForm(forms.Form):
    title       = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle    = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 3}))
    count       = forms.ChoiceField(label='Количество', choices=[
        ('4','4'), ('6','6'), ('8','8'), ('9','9'), ('12','12'), ('all','Все'),
    ])
    display     = forms.ChoiceField(label='Отображение', choices=[
        ('grid', 'Сетка'), ('list', 'Список'),
    ])


class ProductsSectionForm(forms.Form):
    title       = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle    = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 3}))
    display     = forms.ChoiceField(label='Отображение', choices=[
        ('grid', 'Сетка'), ('list', 'Список'),
    ])


class TextImageSectionForm(forms.Form):
    title    = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    body     = forms.CharField(label='Текст', required=False,
                               widget=forms.Textarea(attrs={'rows': 5}))
    layout   = forms.ChoiceField(label='Расположение', choices=[
        ('img_right',  'Текст слева, фото справа'),
        ('img_left',   'Фото слева, текст справа'),
        ('text_top',   'Текст сверху, фото снизу — по центру'),
        ('img_top',    'Фото сверху, текст снизу — по центру'),
        ('text_only',  'Нет фото, текст по центру'),
        ('img_only',   'Нет текста, фото по центру'),
    ])


class StepsSectionForm(forms.Form):
    title       = forms.CharField(label='Заголовок блока', max_length=255, required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Как это работает'}))
    subtitle    = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 3}))


class ContactsSectionForm(forms.Form):
    title         = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle      = forms.CharField(label='Подзаголовок', max_length=255, required=False)
    description   = forms.CharField(label='Текст', required=False,
                                    widget=forms.Textarea(attrs={'rows': 3}))
    contacts_side = forms.ChoiceField(label='Расположение контактов', choices=[
        ('none',          'Не показывать'),
        ('left',          'Слева'),
        ('right',         'Справа'),
        ('top',           'Контакты сверху, адреса снизу — по центру'),
        ('center',        'По центру (без адресов)'),
    ])
    address_side  = forms.ChoiceField(label='Расположение адресов', choices=[
        ('none',          'Не показывать'),
        ('right',         'Справа'),
        ('left',          'Слева'),
        ('bottom',        'Адреса снизу, контакты сверху — по центру'),
        ('center',        'По центру (без контактов)'),
    ])


class MapSectionForm(forms.Form):
    title   = forms.CharField(label='Заголовок', max_length=255, required=False)
    subtitle= forms.CharField(label='Подзаголовок', max_length=255, required=False)
    body    = forms.CharField(label='Текст', required=False,
                              widget=forms.Textarea(attrs={'rows': 3}))
    map_url = forms.CharField(
        label='Ссылка для встраивания Яндекс Карты',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'https://yandex.ru/map-widget/v1/?...',
        }),
        help_text=(
            '1. Откройте Яндекс Карты и найдите адрес\n'
            '2. Нажмите «Поделиться» → «Встроить на сайт»\n'
            '3. Скопируйте значение атрибута src из iframe'
        ),
    )


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


def get_section_form(section_type, data=None, initial=None):
    form_class = SECTION_FORM_MAP.get(section_type)
    if not form_class:
        return None
    if data is not None:
        return form_class(data, initial=initial, prefix='settings')
    return form_class(initial=initial, prefix='settings')