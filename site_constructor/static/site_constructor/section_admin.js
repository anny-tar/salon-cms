(function($) {
    'use strict';

    const SECTION_FIELDS = {
        banner: {
            title: { label: 'Заголовок', type: 'text', placeholder: 'Добро пожаловать в наш салон' },
            subtitle: { label: 'Подзаголовок', type: 'text', placeholder: 'Краткое описание' },
            cta_text: { label: 'Текст кнопки', type: 'text', placeholder: 'Записаться' },
            cta_link: { label: 'Ссылка кнопки', type: 'text', placeholder: '#booking' },
            image: { label: 'Фоновое фото (URL или путь)', type: 'text', placeholder: '' },
        },
        services: {
            count: { label: 'Количество услуг', type: 'select', options: [4, 6, 8, 12] },
            display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
        },
        team: {
            count: { label: 'Количество специалистов', type: 'select', options: [4, 6, 8, 'all:Все'] },
            display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
        },
        portfolio: {
            count: { label: 'Количество работ', type: 'select', options: [6, 9, 12, 'all:Все'] },
            display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'ribbon:Лента'] },
        },
        news: {
            count: { label: 'Количество новостей', type: 'select', options: [3, 6, 9, 12] },
            display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
        },
        products: {
            count: { label: 'Количество товаров', type: 'select', options: [4, 6, 8, 12] },
            display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
        },
        text_image: {
            title: { label: 'Заголовок', type: 'text', placeholder: '' },
            body: { label: 'Текст', type: 'textarea', placeholder: '' },
            image_position: { label: 'Расположение фото', type: 'select', options: ['left:Слева', 'right:Справа'] },
        },
        steps: {
            title: { label: 'Заголовок блока', type: 'text', placeholder: 'Как это работает' },
            steps_json: { label: 'Шаги (JSON)', type: 'textarea', placeholder: '[{"title":"Запись","text":"Выберите услугу онлайн"},{"title":"Визит","text":"Приходите в салон"}]' },
        },
        table: {
            title: { label: 'Заголовок таблицы', type: 'text', placeholder: '' },
            table_json: { label: 'Данные (JSON)', type: 'textarea', placeholder: '{"headers":["Услуга","Цена"],"rows":[["Маникюр","2500 руб."]]}' },
        },
        booking: {
            title: { label: 'Заголовок', type: 'text', placeholder: 'Запишитесь онлайн' },
            show_map: { label: 'Показывать карту (true/false)', type: 'text', placeholder: 'false' },
        },
    };

    function buildForm(type, container, currentSettings) {
        const fields = SECTION_FIELDS[type];
        if (!fields) return;

        let html = '<div class="section-dynamic-fields" style="background:#f8f8f8; padding:12px; border-radius:6px; margin-top:8px;">';
        html += '<p style="font-weight:bold; margin-bottom:10px; color:#333;">Настройки секции:</p>';

        for (const [key, field] of Object.entries(fields)) {
            const val = currentSettings[key] || '';
            html += `<div style="margin-bottom:10px;">`;
            html += `<label style="display:block; font-weight:500; margin-bottom:4px; color:#555;">${field.label}</label>`;

            if (field.type === 'text') {
                html += `<input type="text" data-key="${key}" value="${val}" placeholder="${field.placeholder || ''}"
                          style="width:100%; padding:6px 8px; border:1px solid #ccc; border-radius:4px;">`;
            } else if (field.type === 'textarea') {
                html += `<textarea data-key="${key}" rows="3" placeholder="${field.placeholder || ''}"
                          style="width:100%; padding:6px 8px; border:1px solid #ccc; border-radius:4px;">${val}</textarea>`;
            } else if (field.type === 'select') {
                html += `<select data-key="${key}" style="width:100%; padding:6px 8px; border:1px solid #ccc; border-radius:4px;">`;
                for (const opt of field.options) {
                    if (typeof opt === 'string' && opt.includes(':')) {
                        const [optVal, optLabel] = opt.split(':');
                        html += `<option value="${optVal}" ${val == optVal ? 'selected' : ''}>${optLabel}</option>`;
                    } else {
                        html += `<option value="${opt}" ${val == opt ? 'selected' : ''}>${opt}</option>`;
                    }
                }
                html += '</select>';
            }
            html += '</div>';
        }
        html += '</div>';

        container.html(html);

        // При изменении любого поля — обновляем JSON в скрытом textarea
        container.find('input, textarea, select').on('change input', function() {
            syncToJson(container, fields);
        });
    }

    function syncToJson(container, fields) {
        const result = {};
        container.find('[data-key]').each(function() {
            result[$(this).data('key')] = $(this).val();
        });
        // Находим исходный textarea settings и записываем туда JSON
        container.closest('.inline-related').find('textarea[name$="-settings"]').val(JSON.stringify(result));
    }

    function initSection(row) {
        const typeSelect = row.find('select[name$="-type"]');
        const settingsTextarea = row.find('textarea[name$="-settings"]');

        // Скрываем оригинальный textarea
        settingsTextarea.closest('.form-row').hide();

        let dynamicContainer = row.find('.section-dynamic-fields-container');
        if (!dynamicContainer.length) {
            dynamicContainer = $('<div class="section-dynamic-fields-container"></div>');
            settingsTextarea.closest('.form-row').after(dynamicContainer);
        }

        function render() {
            const type = typeSelect.val();
            let currentSettings = {};
            try { currentSettings = JSON.parse(settingsTextarea.val() || '{}'); } catch(e) {}
            buildForm(type, dynamicContainer, currentSettings);
        }

        typeSelect.on('change', render);
        render();
    }

    $(document).ready(function() {
        // Инициализируем существующие секции
        $('.inline-related').not('.empty-form').each(function() {
            initSection($(this));
        });

        // Инициализируем новые секции при добавлении
        $(document).on('formset:added', function(event, $row) {
            initSection($row);
        });
    });

})(django.jQuery);