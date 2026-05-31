from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'public'

urlpatterns = [
    path('', views.index, name='index'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('specialist/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('ajax/slots/', views.get_available_slots, name='get_slots'),
    path('ajax/book/', views.book_appointment, name='book'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('services/', views.services_page, name='services'),
    path('team/', views.team_page, name='team'),
    path('news/', views.news_page, name='news'),
    path('products/', views.products_page, name='products'),
]