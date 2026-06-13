/**
 * specialist_admin.js
 * Управление портфолио специалиста в Django admin:
 * — кнопки «Скрыть всё» / «Показать всё» в карточке
 * — диалог при деактивации (по диплому)
 */

document.addEventListener('DOMContentLoaded', function () {

    const specialistPk = document.querySelector('[data-specialist-pk]')?.dataset.specialistPk
        || (() => {
            // Берём pk из URL: /admin/specialists/specialist/5/change/
            const m = window.location.pathname.match(/\/specialist\/(\d+)\/change/);
            return m ? m[1] : null;
        })();

    if (!specialistPk) return;

    const actionUrl = `/admin/specialists/specialist/${specialistPk}/portfolio-action/`;
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

    // ── Вспомогательная функция AJAX ────────────────────────────────
    function portfolioAction(action, onSuccess) {
        const form = new FormData();
        form.append('action', action);
        form.append('csrfmiddlewaretoken', csrfToken);

        fetch(actionUrl, { method: 'POST', body: form })
            .then(r => r.json())
            .then(data => {
                if (data.ok) onSuccess(data);
                else alert('Ошибка: ' + (data.error || 'неизвестная'));
            })
            .catch(() => alert('Ошибка соединения'));
    }

    function updateCounters(visible, hidden) {
        const vc = document.getElementById('visible-count');
        const hc = document.getElementById('hidden-count');
        if (vc) vc.textContent = visible;
        if (hc) hc.textContent = hidden;

        const btnHide = document.getElementById('btn-hide-portfolio');
        const btnShow = document.getElementById('btn-show-portfolio');
        if (btnHide) btnHide.disabled = visible === 0;
        if (btnShow) btnShow.disabled = hidden === 0;
    }

    function showFeedback(text) {
        const el = document.getElementById('portfolio-feedback');
        if (!el) return;
        el.textContent = text;
        el.style.display = 'block';
        setTimeout(() => { el.style.display = 'none'; }, 3000);
    }

    // ── Кнопка «Скрыть всё» ─────────────────────────────────────────
    const btnHide = document.getElementById('btn-hide-portfolio');
    if (btnHide) {
        btnHide.addEventListener('click', function () {
            if (!confirm('Скрыть все работы специалиста с публичного сайта?')) return;
            portfolioAction('hide', function (data) {
                const was = parseInt(document.getElementById('visible-count').textContent) || 0;
                updateCounters(0, parseInt(document.getElementById('hidden-count').textContent) + was);
                showFeedback(`Скрыто работ: ${data.hidden}`);
            });
        });
    }

    // ── Кнопка «Показать всё» ───────────────────────────────────────
    const btnShow = document.getElementById('btn-show-portfolio');
    if (btnShow) {
        btnShow.addEventListener('click', function () {
            if (!confirm('Показать все работы специалиста на публичном сайте?')) return;
            portfolioAction('show', function (data) {
                const was = parseInt(document.getElementById('hidden-count').textContent) || 0;
                updateCounters(parseInt(document.getElementById('visible-count').textContent) + was, 0);
                showFeedback(`Показано работ: ${data.shown}`);
            });
        });
    }

    // ── Диалог при деактивации ───────────────────────────────────────
    const isActiveCheckbox = document.getElementById('id_is_active');
    const modal            = document.getElementById('deactivation-modal');

    if (!isActiveCheckbox || !modal) return;

    let wasActive = isActiveCheckbox.checked;

    isActiveCheckbox.addEventListener('change', function () {
        const nowActive = this.checked;

        // Специалиста деактивируют (был активен → стал неактивен)
        if (wasActive && !nowActive) {
            // Проверяем — есть ли вообще видимые работы
            const visibleCount = parseInt(document.getElementById('visible-count')?.textContent) || 0;

            if (visibleCount > 0) {
                // Показываем модальное окно
                modal.style.display = 'flex';
            }
            // Если работ нет — диалог не нужен, просто сохраняем
        }

        wasActive = nowActive;
    });

    // ── Кнопки модального окна ────────────────────────────────────────

    document.getElementById('modal-hide')?.addEventListener('click', function () {
        portfolioAction('hide', function (data) {
            const was = parseInt(document.getElementById('visible-count').textContent) || 0;
            updateCounters(0, parseInt(document.getElementById('hidden-count').textContent) + was);
            showFeedback(`Портфолио скрыто. Скрыто работ: ${data.hidden}`);
        });
        modal.style.display = 'none';
    });

    document.getElementById('modal-keep')?.addEventListener('click', function () {
        modal.style.display = 'none';
        showFeedback('Портфолио оставлено видимым.');
    });

    document.getElementById('modal-cancel')?.addEventListener('click', function () {
        // Возвращаем галочку обратно — пользователь передумал
        isActiveCheckbox.checked = true;
        wasActive = true;
        modal.style.display = 'none';
    });

    // Закрытие по клику на фон
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            isActiveCheckbox.checked = true;
            wasActive = true;
            modal.style.display = 'none';
        }
    });
});