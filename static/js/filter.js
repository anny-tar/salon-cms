/**
 * filter.js — клиентская фильтрация с Select2
 */
'use strict';

(function () {

    // Инициализируем Select2 на всех select с классом select2-filter
    if (window.$ && $.fn.select2) {
        $('.select2-filter').select2({
            theme: 'bootstrap-5',
            allowClear: true,
            width: '100%',
            language: {
                noResults: function() { return 'Ничего не найдено'; },
                searching: function() { return 'Поиск...'; },
            },
        }).on('change', applyFilters);
    }

    function getVal(id) {
        var el = document.getElementById(id);
        if (!el) return '';
        return el.value.toLowerCase().trim();
    }

    function applyFilters() {
        var q          = getVal('filter-search');
        var category   = getVal('filter-category');
        var specialist = getVal('filter-specialist');
        var type       = getVal('filter-type');
        var service    = getVal('filter-service');

        var items = document.querySelectorAll('[data-filter-item]');
        var found = 0;

        items.forEach(function (item) {
            var name     = (item.dataset.name       || '').toLowerCase();
            var cat      = (item.dataset.category   || '').toLowerCase();
            var spec     = (item.dataset.specialist || '').toLowerCase();
            var itype    = (item.dataset.type       || '').toLowerCase();
            var svc      = (item.dataset.service    || '').toLowerCase();

            var match = true;
            if (q          && !name.includes(q))  match = false;
            if (category   && cat  !== category)  match = false;
            if (specialist && spec !== specialist) match = false;
            if (type       && itype !== type)      match = false;
            if (service    && svc  !== service)    match = false;

            item.style.display = match ? '' : 'none';
            if (match) found++;
        });

        var noResults = document.getElementById('no-results');
        if (noResults) noResults.classList.toggle('d-none', found > 0);
    }

    // Текстовые поля
    var searchEl = document.getElementById('filter-search');
    if (searchEl) searchEl.addEventListener('input', applyFilters);

    // Обычные select (если Select2 не инициализирован)
    ['filter-category', 'filter-specialist', 'filter-type', 'filter-service'].forEach(function(id) {
        var el = document.getElementById(id);
        if (el && !(window.$ && $.fn.select2)) {
            el.addEventListener('change', applyFilters);
        }
    });

})();