from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),

    # Страницы-списки
    path('services/',  views.services_page,  name='services'),
    path('team/',      views.team_page,      name='team'),
    path('portfolio/', views.portfolio,      name='portfolio'),
    path('news/',      views.news_page,      name='news'),
    path('products/',  views.products_page,  name='products'),

    # Карточки по slug
    path('specialist/<slug:slug>/', views.specialist_detail, name='specialist_detail'),
    path('service/<slug:slug>/',    views.service_detail,    name='service_detail'),
    path('news/<slug:slug>/',       views.news_detail,       name='news_detail'),
    path('product/<slug:slug>/',    views.product_detail,    name='product_detail'),
    path('portfolio/<slug:slug>/',  views.portfolio_detail,  name='portfolio_detail'),

    # AJAX
    path('ajax/slots/',                      views.get_slots,                   name='get_slots'),
    path('ajax/book/',                       views.book_appointment,             name='book'),
    path('ajax/services-for-specialist/',    views.get_services_for_specialist,  name='services_for_specialist'),
    path('ajax/specialists-for-service/',    views.get_specialists_for_service,  name='specialists_for_service'),
    path('specialist-list-json/',            views.specialist_list_json,         name='specialist_list_json'),

    # Авторизация
    path('login/',  auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]