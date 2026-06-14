from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from specialists.models import Specialist
from services.models import Service
from news.models import Post
from products.models import Product
from portfolio.models import PortfolioWork


class StaticViewSitemap(Sitemap):
    """Статические страницы."""
    priority   = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['public:index', 'public:services', 'public:team',
                'public:portfolio', 'public:news', 'public:products']

    def location(self, item):
        return reverse(item)


class SpecialistSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.7

    def items(self):
        return Specialist.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority   = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)


class NewsSitemap(Sitemap):
    changefreq = 'daily'
    priority   = 0.6

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.created_at


class ProductSitemap(Sitemap):
    changefreq = 'monthly'
    priority   = 0.5

    def items(self):
        return Product.objects.filter(is_active=True)


class PortfolioSitemap(Sitemap):
    changefreq = 'weekly'
    priority   = 0.5

    def items(self):
        return PortfolioWork.objects.filter(is_visible=True)

    def lastmod(self, obj):
        return obj.updated_at