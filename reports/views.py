from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now
from appointments.models import Appointment
from specialists.models import Specialist
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO
from django.core.exceptions import PermissionDenied


def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not (request.user.is_superuser or request.user.groups.filter(name='Владелец').exists()):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

@owner_required
def income_report(request):
    specialists = Specialist.objects.filter(is_active=True)
    selected_specialist_id = request.GET.get('specialist')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    appointments = Appointment.objects.filter(
        status=Appointment.STATUS_COMPLETED
    ).select_related('client', 'specialist', 'service')

    if selected_specialist_id:
        appointments = appointments.filter(specialist_id=selected_specialist_id)
    if date_from:
        appointments = appointments.filter(date__gte=date_from)
    if date_to:
        appointments = appointments.filter(date__lte=date_to)

    # Если нажата кнопка скачать — генерируем Excel
    if 'download' in request.GET:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Отчёт по доходу'

        # Заголовки
        headers = ['Дата', 'Специалист', 'Клиент', 'Услуга', 'Цена (руб.)']
        header_font = Font(bold=True, color='FFFFFF')
        header_fill = PatternFill(fill_type='solid', fgColor='4F81BD')

        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')

        # Данные
        total = 0
        for row, appt in enumerate(appointments, start=2):
            ws.cell(row=row, column=1, value=str(appt.date))
            ws.cell(row=row, column=2, value=appt.specialist.full_name)
            ws.cell(row=row, column=3, value=appt.client.full_name)
            ws.cell(row=row, column=4, value=appt.service.name)
            ws.cell(row=row, column=5, value=float(appt.service.price))
            total += appt.service.price

        # Итоговая строка
        total_row = appointments.count() + 2
        ws.cell(row=total_row, column=4, value='Итого:').font = Font(bold=True)
        ws.cell(row=total_row, column=5, value=float(total)).font = Font(bold=True)

        # Ширина колонок
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['D'].width = 30
        ws.column_dimensions['E'].width = 15

        # Отдаём файл
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        filename = f'отчёт_{now().strftime("%Y-%m-%d")}.xlsx'
        response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    context = {
        'specialists': specialists,
        'appointments': appointments,
        'selected_specialist_id': selected_specialist_id,
        'date_from': date_from,
        'date_to': date_to,
        'total': sum(a.service.price for a in appointments),
    }
    return render(request, 'reports/income.html', context)