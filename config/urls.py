from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', include('reports.urls')),
    path('specialist/', include('specialists.urls')),
    path('', include('public_site.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Кастомные страницы ошибок
# Django ищет эти переменные в корневом urls.py
handler400 = 'public_site.error_views.handler400'
handler403 = 'public_site.error_views.handler403'
handler404 = 'public_site.error_views.handler404'
handler500 = 'public_site.error_views.handler500'