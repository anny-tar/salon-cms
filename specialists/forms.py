from django import forms
from .models import Specialist


class SpecialistAdminForm(forms.ModelForm):
    """Форма специалиста для Django admin."""

    class Meta:
        model  = Specialist
        fields = '__all__'