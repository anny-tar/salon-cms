from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
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
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()

    appointments = Appointment.objects.filter(
        specialist=specialist,
        date=selected_date,
    ).select_related('client', 'service').order_by('time_start')

    context = {
        'specialist': specialist,
        'appointments': appointments,
        'selected_date': selected_date,
    }
    return render(request, 'specialists/schedule.html', context)


@login_required
def appointment_detail(request, pk):
    try:
        specialist = request.user.specialist
    except Specialist.DoesNotExist:
        return redirect('specialists:my_schedule')

    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        specialist=specialist,
    )

    # Загрузка фото доступна только если визит завершён
    is_completed = appointment.status == Appointment.STATUS_COMPLETED
    has_consent = False
    if is_completed:
        has_consent = PhotoConsent.objects.filter(appointment=appointment).exists()

    past_works = PortfolioWork.objects.filter(
        specialist=specialist,
        appointment__client=appointment.client,
        is_visible=True,
    ).order_by('-work_date')[:6]

    context = {
        'appointment': appointment,
        'is_completed': is_completed,
        'has_consent': has_consent,
        'past_works': past_works,
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
        return JsonResponse({'success': False, 'error': 'Нет согласия клиента на публикацию фото'}, status=403)

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

    if request.method == 'POST':
        photo = request.FILES.get('photo')
        category_id = request.POST.get('category')
        liability = request.POST.get('liability')

        if not photo:
            return render(request, 'specialists/upload_direct.html', {
                'categories': ServiceCategory.objects.all(),
                'error': 'Выберите фото',
            })

        if not liability:
            return render(request, 'specialists/upload_direct.html', {
                'categories': ServiceCategory.objects.all(),
                'error': 'Необходимо принять ответственность за публикацию',
            })

        PortfolioWork.objects.create(
            specialist=specialist,
            service_category_id=category_id if category_id else None,
            source=PortfolioWork.SOURCE_DIRECT,
            photo_original=photo,
            work_date=timezone.now().date(),
            specialist_liability=True,
            liability_datetime=timezone.now(),
            is_visible=True,
        )
        return render(request, 'specialists/upload_direct.html', {
            'categories': ServiceCategory.objects.all(),
            'success': True,
        })

    from services.models import ServiceCategory
    return render(request, 'specialists/upload_direct.html', {
        'categories': ServiceCategory.objects.all(),
    })