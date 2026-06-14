from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from appointments.models import Appointment
from portfolio.models import PhotoConsent, PortfolioWork
from .models import Specialist


@login_required
def my_schedule(request):
    try:
        specialist = request.user.specialist
    except Specialist.DoesNotExist:
        return render(request, 'specialists/no_specialist.html')

    date_str = request.GET.get('date')
    today = timezone.now().date()
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    appointments = Appointment.objects.filter(
        specialist=specialist,
        date=selected_date,
    ).select_related('client', 'service').prefetch_related('reference_photos').order_by('time_start')

    completed_count = appointments.filter(status=Appointment.STATUS_COMPLETED).count()
    cancelled_count = appointments.filter(
        status__in=[Appointment.STATUS_CANCELLED, Appointment.STATUS_NO_SHOW]
    ).count()

    context = {
        'specialist':       specialist,
        'appointments':     appointments,
        'selected_date':    selected_date,
        'today':            today,
        'prev_date':        selected_date - timedelta(days=1),
        'next_date':        selected_date + timedelta(days=1),
        'completed_count':  completed_count,
        'cancelled_count':  cancelled_count,
    }
    return render(request, 'specialists/schedule.html', context)


@login_required
def appointment_detail(request, pk):
    try:
        specialist = request.user.specialist
    except Specialist.DoesNotExist:
        return redirect('specialists:my_schedule')

    appointment = get_object_or_404(
        Appointment, pk=pk, specialist=specialist,
    )

    is_completed = appointment.status == Appointment.STATUS_COMPLETED
    has_consent = False
    if is_completed:
        has_consent = PhotoConsent.objects.filter(appointment=appointment).exists()

    past_works = PortfolioWork.objects.filter(
        specialist=specialist,
        appointment__client=appointment.client,
        is_visible=True,
    ).order_by('-work_date')[:6]

    client_visits_count = Appointment.objects.filter(
        client=appointment.client,
        specialist=specialist,
        status=Appointment.STATUS_COMPLETED,
    ).count()

    context = {
        'appointment':        appointment,
        'is_completed':       is_completed,
        'has_consent':        has_consent,
        'past_works':         past_works,
        'client_visits_count': client_visits_count,
    }
    return render(request, 'specialists/appointment_detail.html', context)


@login_required
def upload_photo(request, pk):
    try:
        specialist = request.user.specialist
    except Specialist.DoesNotExist:
        return redirect('specialists:my_schedule')

    appointment = get_object_or_404(Appointment, pk=pk, specialist=specialist)

    if not PhotoConsent.objects.filter(appointment=appointment).exists():
        return JsonResponse(
            {'success': False, 'error': 'Нет согласия клиента на публикацию фото'}, status=403
        )

    if request.method == 'POST':
        photo = request.FILES.get('photo')
        if not photo:
            return JsonResponse({'success': False, 'error': 'Фото не выбрано'})

        PortfolioWork.objects.create(
            specialist=specialist,
            appointment=appointment,
            service_category=appointment.service.category,
            source=PortfolioWork.SOURCE_APPOINTMENT,
            photo_original=photo,
            work_date=appointment.date,
            is_visible=True,
        )
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})


@login_required
def change_status(request, pk):
    try:
        specialist = request.user.specialist
    except Specialist.DoesNotExist:
        return redirect('specialists:my_schedule')

    appointment = get_object_or_404(Appointment, pk=pk, specialist=specialist)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        allowed = [
            Appointment.STATUS_IN_PROGRESS,
            Appointment.STATUS_COMPLETED,
            Appointment.STATUS_NO_SHOW,
        ]
        if new_status in allowed:
            appointment.status = new_status
            appointment.save()
        return redirect('specialists:appointment_detail', pk=pk)

    return redirect('specialists:appointment_detail', pk=pk)


@login_required
def upload_direct(request):
    try:
        specialist = request.user.specialist
    except Specialist.DoesNotExist:
        return redirect('specialists:my_schedule')

    from services.models import ServiceCategory
    today = timezone.now().date()
    categories = ServiceCategory.objects.all()

    if request.method == 'POST':
        photo       = request.FILES.get('photo')
        category_id = request.POST.get('category')
        liability   = request.POST.get('liability')
        work_date_str = request.POST.get('work_date')

        if not photo:
            return render(request, 'specialists/upload_direct.html',
                          {'categories': categories, 'today': today, 'error': 'Выберите фото'})

        if not liability:
            return render(request, 'specialists/upload_direct.html',
                          {'categories': categories, 'today': today,
                           'error': 'Необходимо принять ответственность за публикацию'})

        try:
            work_date = datetime.strptime(work_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            work_date = today

        PortfolioWork.objects.create(
            specialist=specialist,
            service_category_id=category_id if category_id else None,
            source=PortfolioWork.SOURCE_DIRECT,
            photo_original=photo,
            work_date=work_date,
            specialist_liability=True,
            liability_datetime=timezone.now(),
            is_visible=True,
        )
        return redirect('specialists:upload_direct_success')

    return render(request, 'specialists/upload_direct.html',
                  {'categories': categories, 'today': today})


@login_required
def upload_direct_success(request):
    from services.models import ServiceCategory
    today = timezone.now().date()
    return render(request, 'specialists/upload_direct.html', {
        'categories': ServiceCategory.objects.all(),
        'today': today,
        'success': True,
    })