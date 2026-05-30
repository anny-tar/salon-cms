from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('income/', views.income_report, name='income'),
]