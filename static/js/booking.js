/**
 * booking.js — умная форма онлайн-записи.
 * Принимает prefix ('mb' для модала, 'sb' для секции contacts).
 */
'use strict';

function initBookingForm(prefix) {
    var p = prefix;
    var csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value
            || document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

    var selService = document.getElementById(p + '-service');
    var selSpec    = document.getElementById(p + '-specialist');
    var inpDate    = document.getElementById(p + '-date');
    var selTime    = document.getElementById(p + '-time');
    var chkConsent = document.getElementById(p + '-consent');
    var btnSubmit  = document.getElementById(p + '-submit');

    if (!btnSubmit) return;

    // Минимальная дата — сегодня
    var today = new Date().toISOString().split('T')[0];
    if (inpDate) inpDate.min = today;

    // Маска телефона
    var phoneEl = document.getElementById(p + '-phone');
    if (phoneEl && window.IMask) {
        IMask(phoneEl, { mask: '+{7} (000) 000-00-00', lazy: false });
    }

    // ── Загрузка услуг ────────────────────────────────────────────────
    function loadServices() {
        var specId = selSpec?.value;
        fetch('/ajax/available-services/' + (specId ? '?specialist=' + specId : ''))
            .then(function(r) { return r.json(); })
            .then(function(data) {
                var cur = selService.value;
                selService.innerHTML = '<option value="">Выберите услугу</option>';
                data.services.forEach(function(s) {
                    var o = document.createElement('option');
                    o.value = s.id;
                    o.textContent = s.name + ' — ' + s.price + ' ₽ (' + s.duration + ' мин.)';
                    if (s.id == cur) o.selected = true;
                    selService.appendChild(o);
                });
            });
    }

    // ── Загрузка мастеров ─────────────────────────────────────────────
    function loadSpecialists() {
        var serviceId = selService?.value;
        var date      = inpDate?.value;
        var url = '/ajax/available-specialists/?';
        if (serviceId) url += 'service=' + serviceId + '&';
        if (date)      url += 'date=' + date;
        fetch(url)
            .then(function(r) { return r.json(); })
            .then(function(data) {
                var cur = selSpec.value;
                selSpec.innerHTML = '<option value="">Выберите мастера</option>';
                data.specialists.forEach(function(sp) {
                    var o = document.createElement('option');
                    o.value = sp.id;
                    o.textContent = sp.name + ' — ' + sp.specialization;
                    if (sp.id == cur) o.selected = true;
                    selSpec.appendChild(o);
                });
            });
    }

    // ── Загрузка слотов ───────────────────────────────────────────────
    function loadSlots() {
        var specId    = selSpec?.value;
        var serviceId = selService?.value;
        var date      = inpDate?.value;
        selTime.innerHTML = '<option value="">Выберите время</option>';
        if (!specId || !serviceId || !date) {
            selTime.innerHTML = '<option value="">Сначала выберите мастера, услугу и дату</option>';
            return;
        }
        fetch('/ajax/available-slots/?specialist=' + specId +
              '&service=' + serviceId + '&date=' + date)
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.day_off) {
                    selTime.innerHTML = '<option value="">Мастер не работает в этот день</option>';
                } else if (!data.slots || !data.slots.length) {
                    selTime.innerHTML = '<option value="">Нет свободных слотов</option>';
                } else {
                    selTime.innerHTML = '<option value="">Выберите время</option>';
                    data.slots.forEach(function(s) {
                        var o = document.createElement('option');
                        o.value = s; o.textContent = s;
                        selTime.appendChild(o);
                    });
                }
            });
    }

    // ── События ───────────────────────────────────────────────────────
    selService?.addEventListener('change', function() { loadSpecialists(); loadSlots(); });
    selSpec?.addEventListener('change', function() { loadServices(); loadSlots(); });
    inpDate?.addEventListener('change', function() { loadSpecialists(); loadSlots(); });

    // ── Валидация и отправка ──────────────────────────────────────────
    btnSubmit.addEventListener('click', function() {
        var errEl = document.getElementById(p + '-booking-error');
        errEl.classList.add('d-none');

        var errors = [];
        var name  = document.getElementById(p + '-name')?.value.trim();
        var phone = document.getElementById(p + '-phone')?.value.replace(/\D/g, '');
        if (!name)              errors.push('Укажите имя');
        if (phone.length < 11)  errors.push('Укажите корректный номер телефона');
        if (!selService?.value) errors.push('Выберите услугу');
        if (!selSpec?.value)    errors.push('Выберите мастера');
        if (!inpDate?.value)    errors.push('Укажите дату');
        if (!selTime?.value)    errors.push('Выберите время');
        if (!chkConsent?.checked) errors.push('Необходимо согласие на обработку данных');

        if (errors.length) {
            errEl.innerHTML = errors.map(function(e) { return '• ' + e; }).join('<br>');
            errEl.classList.remove('d-none');
            return;
        }

        var fd = new FormData();
        fd.append('full_name',  name);
        fd.append('phone',      document.getElementById(p + '-phone').value);
        fd.append('specialist', selSpec.value);
        fd.append('service',    selService.value);
        fd.append('date',       inpDate.value);
        fd.append('time_start', selTime.value);
        fd.append('pd_consent', 'true');
        fd.append('csrfmiddlewaretoken', csrf);

        var ref1 = document.getElementById(p + '-ref1')?.files[0];
        var ref2 = document.getElementById(p + '-ref2')?.files[0];
        if (ref1) fd.append('reference_photo',   ref1);
        if (ref2) fd.append('reference_photo_2', ref2);

        var captchaToken = document.querySelector('#' + p + '-captcha input[name="smart-token"]')?.value;
        if (captchaToken) fd.append('smart_token', captchaToken);

        fetch('/ajax/book/', { method: 'POST', body: fd })
            .then(function(r) { return r.json(); })
            .then(function(res) {
                if (res.success) {
                    document.getElementById(p + '-booking-form').classList.add('d-none');
                    document.getElementById(p + '-booking-success').classList.remove('d-none');
                    var footer = document.getElementById('modal-footer');
                    if (footer) footer.classList.add('d-none');
                } else {
                    errEl.textContent = res.error || 'Произошла ошибка. Попробуйте ещё раз.';
                    errEl.classList.remove('d-none');
                }
            });
    });

    // Данные загружаются при первом открытии (см. show.bs.modal в base.html)
    // или сразу для встроенной формы (не модал)
    var isModal = !!document.getElementById('bookingModal');
    if (!isModal) {
        loadServices();
        loadSpecialists();
    }
}