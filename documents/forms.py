from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import ProcedureTemplate, ProcedureSection

class ProcedureCreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    template = forms.ModelChoiceField(
        queryset=ProcedureTemplate.objects.filter(is_active=True).order_by("title")
    )

class ProcedureSectionEditForm(forms.ModelForm):
    class Meta:
        model = ProcedureSection
        fields = ["body_html"]

    body_html = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={"style": "width: 100%; min-height: 300px;"}),
    )
