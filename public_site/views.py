from django.shortcuts import render, get_object_or_404
from specialists.models import Specialist
from services.models import Service, ServiceCategory
from portfolio.models import PortfolioWork
from products.models import Product
from news.models import Post
from site_constructor.models import SiteSettings


def index(request):
    settings = SiteSettings.get()
    context = {
        'specialists': Specialist.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True).select_related('category'),
        'categories': ServiceCategory.objects.all(),
        'portfolio': PortfolioWork.objects.filter(is_visible=True).select_related('specialist')[:12],
        'products': Product.objects.filter(is_active=True),
        'posts': Post.objects.filter(is_published=True)[:6],
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