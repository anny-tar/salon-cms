'use strict';

const SECTION_FIELDS = {
    banner: {
        title: { label: 'Заголовок', type: 'text', placeholder: 'Добро пожаловать в наш салон' },
        subtitle: { label: 'Подзаголовок', type: 'text', placeholder: 'Краткое описание' },
        cta_text: { label: 'Текст кнопки', type: 'text', placeholder: 'Записаться' },
        cta_link: { label: 'Ссылка кнопки', type: 'text', placeholder: '#booking' },
    },
    services: {
        count: { label: 'Количество услуг', type: 'select', options: ['4', '6', '8', '12'] },
        display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
    },
    team: {
        count: { label: 'Количество специалистов', type: 'select', options: ['4', '6', '8', 'all:Все'] },
        display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
    },
    portfolio: {
        count: { label: 'Количество работ', type: 'select', options: ['6', '9', '12', 'all:Все'] },
        display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'ribbon:Лента'] },
    },
    news: {
        count: { label: 'Количество новостей', type: 'select', options: ['3', '6', '9', '12'] },
        display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
    },
    products: {
        count: { label: 'Количество товаров', type: 'select', options: ['4', '6', '8', '12'] },
        display: { label: 'Тип отображения', type: 'select', options: ['grid:Сетка', 'list:Список'] },
    },
    text_image: {
        title: { label: 'Заголовок', type: 'text', placeholder: '' },
        body: { label: 'Текст', type: 'textarea', placeholder: '' },
        image_position: { label: 'Расположение фото', type: 'select', options: ['left:Слева', 'right:Справа'] },
    },
    steps: {
        title: { label: 'Заголовок блока', type: 'text', placeholder: 'Как это работает' },
        steps_json: { label: 'Шаги (JSON)', type: 'textarea', placeholder: '[{"title":"Запись","text":"Выберите услугу онлайн"}]' },
    },
    table: {
        title: { label: 'Заголовок таблицы', type: 'text', placeholder: '' },
        table_json: { label: 'Данные (JSON)', type: 'textarea', placeholder: '{"headers":["Услуга","Цена"],"rows":[["Маникюр","2500 руб."]]}' },
    },
    booking: {
        title: { label: 'Заголовок', type: 'text', placeholder: 'Запишитесь онлайн' },
        show_map: { label: 'Показывать карту', type: 'select', options: ['false:Нет', 'true:Да'] },
    },
};

function buildForm(jQ, type, container, currentSettings) {
    const fields = SECTION_FIELDS[type];
    if (!fields) {
        container.html('');
        return;
    }

    let html = '<div style="background:#f0f4f8;padding:14px;border-radius:6px;margin-top:8px;border:1px solid #d0d7de;">';
    html += '<p style="font-weight:600;margin-bottom:12px;color:#24292f;font-size:13px;">⚙ Настройки секции</p>';

    for (const [key, field] of Object.entries(fields)) {
        const val = currentSettings[key] !== undefined ? currentSettings[key] : '';
        html += '<div style="margin-bottom:10px;">';
        html += '<label style="display:block;font-size:12px;font-weight:500;margin-bottom:4px;color:#57606a;">' + field.label + '</label>';

        if (field.type === 'text') {
            html += '<input type="text" data-key="' + key + '" value="' + val + '" placeholder="' + (field.placeholder || '') + '" style="width:100%;padding:6px 10px;border:1px solid #d0d7de;border-radius:4px;font-size:13px;">';
        } else if (field.type === 'textarea') {
            html += '<textarea data-key="' + key + '" rows="3" placeholder="' + (field.placeholder || '') + '" style="width:100%;padding:6px 10px;border:1px solid #d0d7de;border-radius:4px;font-size:12px;font-family:monospace;">' + val + '</textarea>';
        } else if (field.type === 'select') {
            html += '<select data-key="' + key + '" style="width:100%;padding:6px 10px;border:1px solid #d0d7de;border-radius:4px;font-size:13px;">';
            for (const opt of field.options) {
                if (typeof opt === 'string' && opt.includes(':')) {
                    const parts = opt.split(':');
                    html += '<option value="' + parts[0] + '"' + (val === parts[0] ? ' selected' : '') + '>' + parts[1] + '</option>';
                } else {
                    html += '<option value="' + opt + '"' + (val === String(opt) ? ' selected' : '') + '>' + opt + '</option>';
                }
            }
            html += '</select>';
        }
        html += '</div>';
    }
    html += '</div>';

    container.html(html);

    container.find('input, textarea, select').on('change input', function() {
        const result = {};
        container.find('[data-key]').each(function() {
            result[jQ(this).data('key')] = jQ(this).val();
        });
        container.closest('.inline-related').find('textarea[name$="-settings"]').val(JSON.stringify(result, null, 2));
    });
}

function initSection(jQ, row) {
    if (row.data('section-initialized')) return;
    row.data('section-initialized', true);

    // OrderedStackedInline использует другие классы — ищем шире
    const typeSelect = row.find('select').filter(function() {
        return jQ(this).attr('name') && jQ(this).attr('name').indexOf('type') !== -1;
    });
    const settingsTextarea = row.find('textarea').filter(function() {
        return jQ(this).attr('name') && jQ(this).attr('name').indexOf('settings') !== -1;
    });

    if (!typeSelect.length || !settingsTextarea.length) return;

    // Прячем поле settings
    settingsTextarea.closest('div.form-row, p.field-settings, div.field-settings').hide();

    let dynamicContainer = row.find('.section-dynamic-fields-container');
    if (!dynamicContainer.length) {
        dynamicContainer = jQ('<div class="section-dynamic-fields-container"></div>');
        settingsTextarea.parent().after(dynamicContainer);
    }

    function render() {
        const type = typeSelect.val();
        let currentSettings = {};
        try { currentSettings = JSON.parse(settingsTextarea.val() || '{}'); } catch(e) {}
        buildForm(jQ, type, dynamicContainer, currentSettings);
    }

    typeSelect.on('change', render);
    render();
}

function initAll(jQ) {
    function tryInit() {
        jQ('.inline-related').not('.empty-form').each(function() {
            if (!jQ(this).data('section-initialized')) {
                initSection(jQ, jQ(this));
            }
        });
    }

    setTimeout(tryInit, 300);
    setTimeout(tryInit, 800);
    setTimeout(tryInit, 1500);

    jQ(document).on('formset:added', function(event, row) {
        setTimeout(function() { initSection(jQ, jQ(row)); }, 200);
    });

    new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType !== 1) return;
                const el = jQ(node);
                if (el.hasClass('inline-related') && !el.hasClass('empty-form')) {
                    setTimeout(function() { initSection(jQ, el); }, 200);
                }
                el.find('.inline-related').not('.empty-form').each(function() {
                    const child = jQ(this);
                    if (!child.data('section-initialized')) {
                        setTimeout(function() { initSection(jQ, child); }, 200);
                    }
                });
            });
        });
    }).observe(document.body, { childList: true, subtree: true });
}

var waitForJQuery = setInterval(function() {
    if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
        clearInterval(waitForJQuery);
        django.jQuery(document).ready(function() {
            initAll(django.jQuery);
        });
    }
}, 50);
