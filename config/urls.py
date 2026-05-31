from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from site_constructor.views import manage_sections

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/sections/', manage_sections, name='manage_sections'),
    path('reports/', include('reports.urls')),
    path('specialist/', include('specialists.urls')),
    path('', include('public_site.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)