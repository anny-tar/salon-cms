from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('specialist/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('ajax/slots/', views.get_available_slots, name='get_slots'),
    path('ajax/book/', views.book_appointment, name='book'),
]