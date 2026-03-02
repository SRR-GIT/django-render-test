from django import forms
from .models import ProcedureTemplate

class ProcedureCreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    template = forms.ModelChoiceField(
        queryset=ProcedureTemplate.objects.filter(is_active=True).order_by("title")
    )
