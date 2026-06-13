"""
Сервисный слой для расписания и слотов.
Вся бизнес-логика вычисления доступного времени — здесь,
а не во views или моделях.
"""
from datetime import datetime, timedelta
from appointments.models import Appointment


def get_available_slots(specialist, service, date):
    """
    Возвращает список строк доступных слотов ('09:00', '09:30', ...)
    для записи к специалисту на конкретную услугу и дату.

    Возвращает (slots: list[str], day_off: bool).
    """
    hours = specialist.get_hours_for_date(date)
    if hours is None:
        return [], True  # выходной

    work_start = datetime.combine(date, datetime.strptime(hours[0], '%H:%M').time())
    work_end   = datetime.combine(date, datetime.strptime(hours[1], '%H:%M').time())
    duration   = timedelta(minutes=service.duration)

    # Занятые интервалы: только активные записи
    busy = list(
        Appointment.objects.filter(
            specialist=specialist,
            date=date,
            status__in=[
                Appointment.STATUS_PENDING,
                Appointment.STATUS_CONFIRMED,
                Appointment.STATUS_IN_PROGRESS,
            ],
        ).values_list('time_start', 'time_end')
    )

    slots = []
    current = work_start
    while current + duration <= work_end:
        slot_end = current + duration
        is_busy = any(
            current < datetime.combine(date, b_end)
            and slot_end > datetime.combine(date, b_start)
            for b_start, b_end in busy
        )
        if not is_busy:
            slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=30)

    return slots, False