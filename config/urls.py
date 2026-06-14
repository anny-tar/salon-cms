from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from public_site.sitemaps import (
    StaticViewSitemap, SpecialistSitemap, ServiceSitemap,
    NewsSitemap, ProductSitemap, PortfolioSitemap,
)

sitemaps = {
    'static':      StaticViewSitemap,
    'specialists': SpecialistSitemap,
    'services':    ServiceSitemap,
    'news':        NewsSitemap,
    'products':    ProductSitemap,
    'portfolio':   PortfolioSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),
    path('specialist/', include('specialists.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    path('', include('public_site.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Кастомные страницы ошибок
# Django ищет эти переменные в корневом urls.py
handler400 = 'public_site.error_views.handler400'
handler403 = 'public_site.error_views.handler403'
handler404 = 'public_site.error_views.handler404'
handler500 = 'public_site.error_views.handler500'