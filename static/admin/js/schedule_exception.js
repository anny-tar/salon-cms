/**
 * schedule_exception.js
 * Маски для полей времени (ЧЧ:ММ) и даты (дд.мм.гггг)
 * в форме исключений расписания и базовом расписании специалиста.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Маска времени ЧЧ:ММ ──────────────────────────────────────────
    function applyTimeMask(input) {
        input.addEventListener('input', function () {
            // Оставляем только цифры
            let digits = this.value.replace(/\D/g, '').slice(0, 4);
            if (digits.length >= 3) {
                this.value = digits.slice(0, 2) + ':' + digits.slice(2);
            } else {
                this.value = digits;
            }
        });

        input.addEventListener('blur', function () {
            const match = this.value.match(/^(\d{1,2}):?(\d{0,2})$/);
            if (match) {
                const hh = match[1].padStart(2, '0');
                const mm = (match[2] || '00').padStart(2, '0');
                const hNum = parseInt(hh), mNum = parseInt(mm);
                if (hNum >= 0 && hNum <= 23 && mNum >= 0 && mNum <= 59) {
                    this.value = hh + ':' + mm;
                    this.style.borderColor = '';
                } else {
                    this.style.borderColor = '#dc3545';
                }
            } else if (this.value !== '') {
                this.style.borderColor = '#dc3545';
            }
        });

        input.addEventListener('focus', function () {
            this.style.borderColor = '';
        });
    }

    // ── Подсказки для полей is_day_off ────────────────────────────────
    // Когда чекбокс «Выходной день» активен — блокируем поля времени
    function bindDayOffToggle(checkbox) {
        function toggle() {
            const row = checkbox.closest('.inline-related, .form-row, tr');
            if (!row) return;
            const timeInputs = row.querySelectorAll('.schedule-time-input');
            timeInputs.forEach(function (inp) {
                if (checkbox.checked) {
                    inp.disabled = true;
                    inp.style.opacity = '0.4';
                } else {
                    inp.disabled = false;
                    inp.style.opacity = '1';
                }
            });
        }
        checkbox.addEventListener('change', toggle);
        toggle(); // применяем при загрузке
    }

    // ── Инициализация при загрузке страницы ──────────────────────────
    function init() {
        // Поля времени в исключениях и в базовом расписании
        document.querySelectorAll('.schedule-time-input').forEach(applyTimeMask);

        // Чекбоксы is_day_off
        document.querySelectorAll('input[id*="is_day_off"]').forEach(bindDayOffToggle);
    }

    init();

    // ── Поддержка динамически добавляемых inline-строк ───────────────
    // Django добавляет новые строки через событие на document
    document.addEventListener('formset:added', function (event) {
        const row = event.target;
        row.querySelectorAll('.schedule-time-input').forEach(applyTimeMask);
        row.querySelectorAll('input[id*="is_day_off"]').forEach(bindDayOffToggle);
    });
});