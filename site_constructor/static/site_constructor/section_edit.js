'use strict';

const SECTION_FIELDS = {

    banner: {
        title:    { label: 'Заголовок',      type: 'text',   placeholder: 'Добро пожаловать' },
        subtitle: { label: 'Подзаголовок',   type: 'text',   placeholder: 'Краткое описание' },
        cta_text: { label: 'Текст кнопки',   type: 'text',   placeholder: 'Записаться' },
        align:    { label: 'Выравнивание',   type: 'select',
                    options: ['center:По центру', 'left:По левому краю', 'right:По правому краю'] },
        overlay:  { label: 'Маска фона',     type: 'select',
                    options: ['dark:Затемнение', 'light:Осветление', 'none:Без маски'] },
    },

    services: {
        title:       { label: 'Заголовок',   type: 'text',     placeholder: 'Наши услуги' },
        subtitle:    { label: 'Подзаголовок',type: 'text',     placeholder: '' },
        description: { label: 'Описание',    type: 'textarea', placeholder: '' },
        count:       { label: 'Количество',  type: 'select',
                       options: ['4', '6', '8', '9', '12', 'all:Все'] },
        display:     { label: 'Отображение', type: 'select',
                       options: ['grid:Сетка', 'list:Список'] },
    },

    team: {
        title:       { label: 'Заголовок',   type: 'text',     placeholder: 'Наша команда' },
        subtitle:    { label: 'Подзаголовок',type: 'text',     placeholder: '' },
        description: { label: 'Описание',    type: 'textarea', placeholder: '' },
        count:       { label: 'Количество',  type: 'select',
                       options: ['4', '6', '8', 'all:Все'] },
        display:     { label: 'Отображение', type: 'select',
                       options: ['grid:Сетка', 'list:Список'] },
    },

    portfolio: {
        title:       { label: 'Заголовок',   type: 'text',     placeholder: 'Портфолио' },
        subtitle:    { label: 'Подзаголовок',type: 'text',     placeholder: '' },
        description: { label: 'Описание',    type: 'textarea', placeholder: '' },
        count:       { label: 'Количество',  type: 'select',
                       options: ['6', '9', '12', 'all:Все'] },
        display:     { label: 'Отображение', type: 'select',
                       options: ['grid:Сетка', 'ribbon:Лента'] },
    },

    news: {
        title:       { label: 'Заголовок',   type: 'text',     placeholder: 'Новости и акции' },
        subtitle:    { label: 'Подзаголовок',type: 'text',     placeholder: '' },
        description: { label: 'Описание',    type: 'textarea', placeholder: '' },
        count:       { label: 'Количество',  type: 'select',
                       options: ['3', '6', '9', '12'] },
        display:     { label: 'Отображение', type: 'select',
                       options: ['grid:Сетка', 'list:Список'] },
    },

    products: {
        title:       { label: 'Заголовок',   type: 'text',     placeholder: 'Товары' },
        subtitle:    { label: 'Подзаголовок',type: 'text',     placeholder: '' },
        description: { label: 'Описание',    type: 'textarea', placeholder: '' },
        display:     { label: 'Отображение', type: 'select',
                       options: ['grid:Сетка', 'list:Список'] },
    },

    text_image: {
        title:    { label: 'Заголовок',    type: 'text',     placeholder: 'О нас' },
        subtitle: { label: 'Подзаголовок', type: 'text',     placeholder: '' },
        body:     { label: 'Текст',        type: 'textarea', placeholder: 'Расскажите о салоне...' },
        layout:   { label: 'Расположение', type: 'select',
                    options: [
                        'img_right:Текст слева, фото справа',
                        'img_left:Фото слева, текст справа',
                        'img_bottom:Текст сверху, фото снизу',
                    ]},
    },

    steps: {
        title:       { label: 'Заголовок блока', type: 'text',     placeholder: 'Как это работает' },
        subtitle:    { label: 'Подзаголовок',    type: 'text',     placeholder: '' },
        description: { label: 'Описание',        type: 'textarea', placeholder: '' },
        // Сами шаги добавляются через SectionStepInline в admin
    },

    contacts: {
        title:         { label: 'Заголовок',               type: 'text', placeholder: 'Контакты' },
        subtitle:      { label: 'Подзаголовок',            type: 'text', placeholder: '' },
        contacts_side: { label: 'Расположение контактов',  type: 'select',
                         options: ['left:Слева', 'right:Справа', 'none:Не показывать'] },
        phone:         { label: 'Телефон',                 type: 'text', placeholder: '+7 (900) 000-00-00' },
        email:         { label: 'Email',                   type: 'text', placeholder: 'info@salon.ru' },
        vk:            { label: 'ВКонтакте',               type: 'text', placeholder: 'https://vk.com/...' },
        telegram:      { label: 'Telegram',                type: 'text', placeholder: '@username' },
        whatsapp:      { label: 'WhatsApp',                type: 'text', placeholder: '+7 900 000-00-00' },
        instagram:     { label: 'Instagram',               type: 'text', placeholder: 'https://instagram.com/...' },
        form_side:     { label: 'Расположение формы записи', type: 'select',
                         options: ['right:Справа', 'left:Слева', 'none:Не показывать'] },
    },

    map: {
        title:    { label: 'Заголовок',    type: 'text',     placeholder: 'Как нас найти' },
        subtitle: { label: 'Подзаголовок', type: 'text',     placeholder: '' },
        body:     { label: 'Текст',        type: 'textarea', placeholder: 'Описание как добраться...' },
        map_url:  { label: 'Ссылка для встраивания карты (src из iframe)', type: 'textarea',
                    placeholder: 'https://yandex.ru/map-widget/v1/?...' },
    },
};

document.addEventListener('DOMContentLoaded', function () {

    var typeSelect       = document.querySelector('select[name="type"]');
    var settingsTextarea = document.querySelector('textarea[name="settings"]');

    if (!settingsTextarea) return;

    // Тип: из select или из readonly поля
    var currentType = null;
    if (typeSelect) {
        currentType = typeSelect.value;
    } else {
        var TYPE_MAP = {
            'Баннер': 'banner', 'Услуги': 'services', 'О команде': 'team',
            'Портфолио': 'portfolio', 'Новости и акции': 'news', 'Товары': 'products',
            'Текст + Изображение': 'text_image', 'Шаги': 'steps',
            'Контакты и форма': 'contacts', 'Карта': 'map',
        };
        var readonlyEl = document.querySelector('.field-type .readonly');
        if (readonlyEl) currentType = TYPE_MAP[readonlyEl.textContent.trim()];
    }

    if (!currentType) return;

    // Скрываем поле image для секций без изображения
    var imageRow = document.querySelector('.field-image');
    if (imageRow) {
        imageRow.style.display = ['banner', 'text_image'].indexOf(currentType) !== -1 ? '' : 'none';
    }

    // Скрываем textarea settings
    var settingsRow = settingsTextarea.closest('.field-settings') ||
                      settingsTextarea.closest('.form-row') ||
                      settingsTextarea.parentNode;
    if (settingsRow) settingsRow.style.display = 'none';

    // Для секции steps — поясняем что шаги в inline
    if (currentType === 'steps') {
        var stepsNote = document.createElement('div');
        stepsNote.style.cssText = 'margin:8px 0 16px; padding:10px 14px; background:#e8f4fd; border-left:4px solid #417690; border-radius:4px; font-size:13px;';
        stepsNote.innerHTML = '💡 Сами шаги добавляются в блоке <strong>«Шаги»</strong> ниже на этой странице. Здесь настройте заголовок и описание блока.';
        settingsRow.insertAdjacentElement('afterend', stepsNote);
    }

    // Контейнер полей
    var container = document.getElementById('section-fields-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'section-fields-container';
        settingsRow.insertAdjacentElement('afterend', container);
    }

    function getCurrentValues() {
        try { return JSON.parse(settingsTextarea.value || '{}'); }
        catch (e) { return {}; }
    }

    function syncToTextarea() {
        var result = {};
        container.querySelectorAll('[data-key]').forEach(function (el) {
            result[el.dataset.key] = el.value;
        });
        settingsTextarea.value = JSON.stringify(result);
    }

    function render() {
        var type    = currentType;
        if (typeSelect) type = typeSelect.value;
        var fields  = SECTION_FIELDS[type];
        var current = getCurrentValues();

        if (!fields || Object.keys(fields).length === 0) {
            container.innerHTML = '';
            return;
        }

        var html = '<fieldset class="module aligned" style="margin-top:0;">';

        Object.keys(fields).forEach(function (key) {
            var field   = fields[key];
            var val     = current[key] !== undefined ? current[key] : '';
            var safeVal = String(val).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');

            html += '<div class="form-row"><div>';
            html += '<label style="font-weight:600;">' + field.label + ':</label>';

            if (field.type === 'text') {
                html += '<input type="text" data-key="' + key + '" value="' + safeVal + '"'
                      + ' placeholder="' + (field.placeholder || '') + '"'
                      + ' class="vTextField">';

            } else if (field.type === 'textarea') {
                html += '<textarea data-key="' + key + '" rows="4"'
                      + ' placeholder="' + (field.placeholder || '') + '"'
                      + ' style="width:100%;max-width:800px;">'
                      + safeVal + '</textarea>';

            } else if (field.type === 'select') {
                html += '<select data-key="' + key + '">';
                field.options.forEach(function (opt) {
                    var v, l;
                    if (opt.indexOf(':') !== -1) {
                        var parts = opt.split(':');
                        v = parts[0]; l = parts.slice(1).join(':');
                    } else { v = opt; l = opt; }
                    html += '<option value="' + v + '"' + (val === v ? ' selected' : '') + '>' + l + '</option>';
                });
                html += '</select>';
            }

            html += '</div></div>';
        });

        html += '</fieldset>';
        container.innerHTML = html;

        syncToTextarea();

        container.querySelectorAll('[data-key]').forEach(function (el) {
            el.addEventListener('input',  syncToTextarea);
            el.addEventListener('change', syncToTextarea);
        });
    }

    if (typeSelect) typeSelect.addEventListener('change', render);
    render();
});