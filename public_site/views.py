from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from specialists.models import Specialist
from services.models import Service, ServiceCategory
from portfolio.models import PortfolioWork
from products.models import Product
from news.models import Post
from site_constructor.models import SiteSettings
from clients.models import Client
from appointments.models import Appointment
from .forms import BookingForm


def index(request):
    from site_constructor.models import SiteSettings, Section
    from specialists.models import Specialist
    from services.models import Service, ServiceCategory
    from portfolio.models import PortfolioWork
    from products.models import Product
    from news.models import Post

    site = SiteSettings.get()
    sections = Section.objects.filter(site=site).order_by('order')

    # Подготавливаем данные для живых секций
    live_data = {
        'specialists': Specialist.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True).select_related('category'),
        'portfolio': PortfolioWork.objects.filter(is_visible=True).select_related('specialist'),
        'news': Post.objects.filter(is_published=True),
        'products': Product.objects.filter(is_active=True),
    }

    context = {
        'sections': sections,
        'live_data': live_data,
        'specialists': live_data['specialists'],  # для формы записи
        'services': live_data['services'],        # для формы записи
        'form': BookingForm(),
    }
    return render(request, 'public/index.html', context)


def portfolio(request):
    works = PortfolioWork.objects.filter(is_visible=True).select_related('specialist', 'service_category')
    specialists = Specialist.objects.filter(is_active=True)
    categories = ServiceCategory.objects.all()

    specialist_id = request.GET.get('specialist')
    category_id = request.GET.get('category')

    if specialist_id:
        works = works.filter(specialist_id=specialist_id)
    if category_id:
        works = works.filter(service_category_id=category_id)

    context = {
        'works': works,
        'specialists': specialists,
        'categories': categories,
        'selected_specialist': specialist_id,
        'selected_category': category_id,
    }
    return render(request, 'public/portfolio.html', context)


def specialist_detail(request, pk):
    specialist = get_object_or_404(Specialist, pk=pk, is_active=True)
    works = PortfolioWork.objects.filter(
        specialist=specialist,
        is_visible=True
    ).select_related('service_category')

    context = {
        'specialist': specialist,
        'works': works,
    }
    return render(request, 'public/specialist.html', context)


def get_available_slots(request):
    """AJAX: возвращает доступные слоты для выбранного специалиста, услуги и даты"""
    specialist_id = request.GET.get('specialist')
    service_id = request.GET.get('service')
    date_str = request.GET.get('date')

    if not all([specialist_id, service_id, date_str]):
        return JsonResponse({'slots': []})

    try:
        specialist = Specialist.objects.get(pk=specialist_id)
        service = Service.objects.get(pk=service_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'slots': []})

    # Рабочие часы — с 9:00 до 20:00 с шагом по длительности услуги
    work_start = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
    work_end = datetime.combine(date, datetime.strptime('20:00', '%H:%M').time())
    duration = timedelta(minutes=service.duration)

    # Занятые интервалы
    busy = Appointment.objects.filter(
        specialist=specialist,
        date=date,
        status__in=[
            Appointment.STATUS_PENDING,
            Appointment.STATUS_CONFIRMED,
            Appointment.STATUS_IN_PROGRESS,
        ]
    ).values_list('time_start', 'time_end')

    # Генерируем свободные слоты
    slots = []
    current = work_start
    while current + duration <= work_end:
        slot_end = current + duration
        is_busy = False
        for b_start, b_end in busy:
            busy_start = datetime.combine(date, b_start)
            busy_end = datetime.combine(date, b_end)
            if current < busy_end and slot_end > busy_start:
                is_busy = True
                break
        if not is_busy:
            slots.append(current.strftime('%H:%M'))
        current += timedelta(minutes=30)

    return JsonResponse({'slots': slots})


def book_appointment(request):
    """Обработка формы онлайн-записи"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})

    phone = request.POST.get('phone', '').strip()
    full_name = request.POST.get('full_name', '').strip()

    if not phone or not full_name:
        return JsonResponse({'success': False, 'error': 'Заполните имя и телефон'})

    if not request.POST.get('pd_consent'):
        return JsonResponse({'success': False, 'error': 'Необходимо согласие на обработку ПД'})

    try:
        specialist = Specialist.objects.get(pk=request.POST.get('specialist'))
        service = Service.objects.get(pk=request.POST.get('service'))
        date = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        time_start = datetime.strptime(request.POST.get('time_start'), '%H:%M').time()
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Некорректные данные: {e}'})

    client, created = Client.objects.get_or_create(
        phone=phone,
        defaults={'full_name': full_name}
    )

    Appointment.objects.create(
        client=client,
        specialist=specialist,
        service=service,
        date=date,
        time_start=time_start,
        status=Appointment.STATUS_PENDING,
        pd_consent_datetime=timezone.now(),
    )

    return JsonResponse({'success': True})