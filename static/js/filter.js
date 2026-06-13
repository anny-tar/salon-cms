/**
 * filter.js — клиентская фильтрация для страниц-списков
 */
'use strict';

(function () {

    function getVal(id) {
        var el = document.getElementById(id);
        return el ? el.value.toLowerCase().trim() : '';
    }

    function applyFilters() {
        var q          = getVal('filter-search');
        var category   = getVal('filter-category');
        var specialist = getVal('filter-specialist');
        var type       = getVal('filter-type');

        var items = document.querySelectorAll('[data-filter-item]');
        var found = 0;

        items.forEach(function (item) {
            var name     = (item.dataset.name       || '').toLowerCase();
            var cat      = (item.dataset.category   || '').toLowerCase();
            var spec     = (item.dataset.specialist || '').toLowerCase();
            var itype    = (item.dataset.type       || '').toLowerCase();

            var match = true;
            if (q          && !name.includes(q))  match = false;
            if (category   && cat  !== category)  match = false;
            if (specialist && spec !== specialist) match = false;
            if (type       && itype !== type)      match = false;

            item.style.display = match ? '' : 'none';
            if (match) found++;
        });

        var noResults = document.getElementById('no-results');
        if (noResults) noResults.classList.toggle('d-none', found > 0);
    }

    ['filter-search', 'filter-category', 'filter-specialist', 'filter-type'].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) {
            el.addEventListener('input',  applyFilters);
            el.addEventListener('change', applyFilters);
        }
    });

})();