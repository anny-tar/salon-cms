from django import forms
from clients.models import Client
from specialists.models import Specialist
from services.models import Service


class BookingForm(forms.Form):
    full_name = forms.CharField(
        label='Ваше имя',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя Фамилия'})
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 000-00-00'})
    )
    specialist = forms.ModelChoiceField(
        label='Специалист',
        queryset=Specialist.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_specialist'})
    )
    service = forms.ModelChoiceField(
        label='Услуга',
        queryset=Service.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_service'})
    )
    date = forms.DateField(
        label='Дата',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_date'})
    )
    time_start = forms.ChoiceField(
        label='Время',
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_time_start'})
    )
    pd_consent = forms.BooleanField(
        label='Согласен на обработку персональных данных',
        required=True,
    )