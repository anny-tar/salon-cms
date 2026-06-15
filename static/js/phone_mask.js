// Маска телефона для полей с data-mask в Django admin
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[data-mask]').forEach(function(el) {
        if (window.IMask) {
            IMask(el, { mask: el.dataset.mask, lazy: false });
        }
    });
});