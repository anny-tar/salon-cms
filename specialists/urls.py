from django.urls import path
from . import views

app_name = 'specialists'

urlpatterns = [
    path('my/', views.my_schedule, name='my_schedule'),
    path('my/appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('my/appointment/<int:pk>/upload-photo/', views.upload_photo, name='upload_photo'),
    path('my/appointment/<int:pk>/change-status/', views.change_status, name='change_status'),
]