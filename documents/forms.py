from django import forms
from .models import ProcedureTemplate, ProcedureSection

class ProcedureCreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    template = forms.ModelChoiceField(
        queryset=ProcedureTemplate.objects.filter(is_active=True).order_by("title")
    )

class ProcedureSectionEditForm(forms.ModelForm):
    class Meta:
        model = ProcedureSection
        fields = ["body_html"]  # ou ["title", "body_html"]
