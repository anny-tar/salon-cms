from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime

from specialists.models import Specialist
from specialists.services import get_available_slots
from services.models import Service, ServiceCategory
from portfolio.models import PortfolioWork
from products.models import Product
from news.models import Post
from site_constructor.models import SiteSettings
from clients.models import Client
from appointments.models import Appointment, AppointmentReferencePhoto


def index(request):
    from site_constructor.models import Section
    site     = SiteSettings.get()
    sections = Section.objects.filter(site=site, is_visible=True).order_by('order')
    live_data = {
        'specialists': Specialist.objects.filter(is_active=True),
        'services':    Service.objects.filter(is_active=True).select_related('category'),
        'portfolio':   PortfolioWork.objects.filter(is_visible=True).select_related('specialist'),
        'news':        Post.objects.filter(is_published=True),
        'products':    Product.objects.filter(is_active=True),
    }
    return render(request, 'public/index.html', {
        'sections':    sections,
        'live_data':   live_data,
        'specialists': live_data['specialists'],
        'services':    live_data['services'],
    })


def portfolio(request):
    works       = PortfolioWork.objects.filter(is_visible=True).select_related('specialist', 'service_category')
    specialists = Specialist.objects.filter(is_active=True)
    categories  = ServiceCategory.objects.all()
    specialist_id = request.GET.get('specialist')
    category_id   = request.GET.get('category')
    if specialist_id:
        works = works.filter(specialist_id=specialist_id)
    if category_id:
        works = works.filter(service_category_id=category_id)
    return render(request, 'public/portfolio.html', {
        'works': works, 'specialists': specialists, 'categories': categories,
        'selected_specialist': specialist_id, 'selected_category': category_id,
    })


def specialist_detail(request, pk):
    specialist = get_object_or_404(Specialist, pk=pk, is_active=True)
    works = PortfolioWork.objects.filter(
        specialist=specialist, is_visible=True,
    ).select_related('service_category')
    categories = ServiceCategory.objects.filter(
        portfoliowork__specialist=specialist,
        portfoliowork__is_visible=True,
    ).distinct()
    selected_category = request.GET.get('category')
    if selected_category:
        works = works.filter(service_category_id=selected_category)
    return render(request, 'public/specialist.html', {
        'specialist': specialist, 'works': works,
        'categories': categories, 'selected_category': selected_category,
        'documents': specialist.documents.all(),
    })


# ── AJAX: фильтрация формы записи ────────────────────────────────────


def specialist_list_json(request):
    """AJAX: список активных специалистов для модала записи."""
    from specialists.models import Specialist
    specialists = Specialist.objects.filter(is_active=True).values('id', 'full_name')
    return JsonResponse({'specialists': list(specialists)})

def get_services_for_specialist(request):
    specialist_id = request.GET.get('specialist')
    if not specialist_id:
        return JsonResponse({'services': []})
    try:
        specialist = Specialist.objects.get(pk=specialist_id, is_active=True)
    except Specialist.DoesNotExist:
        return JsonResponse({'services': []})
    services = specialist.services.filter(is_active=True).values('id', 'name')
    return JsonResponse({'services': list(services)})


def get_specialists_for_service(request):
    service_id = request.GET.get('service')
    if not service_id:
        return JsonResponse({'specialists': []})
    try:
        service = Service.objects.get(pk=service_id, is_active=True)
    except Service.DoesNotExist:
        return JsonResponse({'specialists': []})
    specialists = service.specialists.filter(is_active=True).values('id', 'full_name')
    return JsonResponse({'specialists': list(specialists)})


def get_slots(request):
    """AJAX: доступные слоты. Делегирует логику в specialists.services."""
    specialist_id = request.GET.get('specialist')
    service_id    = request.GET.get('service')
    date_str      = request.GET.get('date')
    if not all([specialist_id, service_id, date_str]):
        return JsonResponse({'slots': []})
    try:
        specialist = Specialist.objects.get(pk=specialist_id)
        service    = Service.objects.get(pk=service_id)
        date       = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        return JsonResponse({'slots': []})
    slots, day_off = get_available_slots(specialist, service, date)
    return JsonResponse({'slots': slots, 'day_off': day_off})


def book_appointment(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Метод не поддерживается'})
    phone     = request.POST.get('phone', '').strip()
    full_name = request.POST.get('full_name', '').strip()
    if not phone or not full_name:
        return JsonResponse({'success': False, 'error': 'Заполните имя и телефон'})
    if not request.POST.get('pd_consent'):
        return JsonResponse({'success': False, 'error': 'Необходимо согласие на обработку ПД'})
    try:
        specialist = Specialist.objects.get(pk=request.POST.get('specialist'))
        service    = Service.objects.get(pk=request.POST.get('service'))
        date       = datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        time_start = datetime.strptime(request.POST.get('time_start'), '%H:%M').time()
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Некорректные данные: {e}'})

    client, _ = Client.objects.get_or_create(phone=phone, defaults={'full_name': full_name})
    appointment = Appointment.objects.create(
        client=client, specialist=specialist, service=service,
        date=date, time_start=time_start,
        status=Appointment.STATUS_PENDING,
        pd_consent_datetime=timezone.now(),
    )
    # Референсы — через отдельную модель
    for key in ('reference_photo', 'reference_photo_2'):
        photo = request.FILES.get(key)
        if photo:
            AppointmentReferencePhoto.objects.create(appointment=appointment, photo=photo)

    return JsonResponse({'success': True})


# ── Страницы сайта ────────────────────────────────────────────────────

def _check_page(page_type):
    from django.http import Http404
    from site_constructor.models import SitePage
    if not SitePage.objects.filter(page_type=page_type, is_visible=True).exists():
        raise Http404


def services_page(request):
    _check_page('services')
    services  = Service.objects.filter(is_active=True).select_related('category')
    categories = ServiceCategory.objects.all()
    selected  = request.GET.get('category')
    if selected:
        services = services.filter(category_id=selected)
    return render(request, 'public/services.html', {
        'services': services, 'categories': categories, 'selected_category': selected,
    })


def team_page(request):
    _check_page('team')
    return render(request, 'public/team.html', {
        'specialists': Specialist.objects.filter(is_active=True),
    })


def news_page(request):
    _check_page('news')
    post_type = request.GET.get('type')
    posts = Post.objects.filter(is_published=True)
    if post_type:
        posts = posts.filter(post_type=post_type)
    return render(request, 'public/news.html', {'posts': posts, 'post_type': post_type})


def products_page(request):
    _check_page('products')
    return render(request, 'public/products.html', {
        'products': Product.objects.filter(is_active=True),
    })


# ── Карточки ──────────────────────────────────────────────────────────

def specialist_detail(request, slug):
    from specialists.models import Specialist
    specialist = get_object_or_404(Specialist, slug=slug, is_active=True)
    works = PortfolioWork.objects.filter(
        specialist=specialist, is_visible=True
    ).select_related('service_category')
    categories = ServiceCategory.objects.filter(
        portfoliowork__specialist=specialist,
        portfoliowork__is_visible=True,
    ).distinct()
    selected_category = request.GET.get('category')
    if selected_category:
        works = works.filter(service_category_id=selected_category)
    return render(request, 'public/specialist.html', {
        'specialist':        specialist,
        'works':             works,
        'categories':        categories,
        'selected_category': selected_category,
        'documents':         specialist.documents.all(),
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    specialists = service.specialists.filter(is_active=True)
    return render(request, 'public/service_detail.html', {
        'service':     service,
        'specialists': specialists,
    })


def news_detail(request, slug):
    from news.models import Post
    post = get_object_or_404(Post, slug=slug, is_published=True)
    related = Post.objects.filter(
        is_published=True, post_type=post.post_type
    ).exclude(pk=post.pk)[:3]
    return render(request, 'public/news_detail.html', {
        'post':    post,
        'related': related,
    })


def product_detail(request, slug):
    from products.models import Product
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = Product.objects.filter(is_active=True).exclude(pk=product.pk)[:4]
    return render(request, 'public/product_detail.html', {
        'product': product,
        'related': related,
    })


def portfolio_detail(request, slug):
    work = get_object_or_404(PortfolioWork, slug=slug, is_visible=True)
    related = PortfolioWork.objects.filter(
        specialist=work.specialist, is_visible=True
    ).exclude(pk=work.pk)[:6]
    return render(request, 'public/portfolio_detail.html', {
        'work':    work,
        'related': related,
    })