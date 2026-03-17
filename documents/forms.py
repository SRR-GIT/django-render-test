from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import ProcedureTemplate, ProcedureSection, ProcedureSectionVariable

class ProcedureSectionEditForm(forms.ModelForm):
    class Meta:
        model = ProcedureSection
        fields = ["body_html"]

    body_html = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={"style": "width: 100%; min-height: 300px;"}),
    )
    
class ProcedureCreateForm(forms.Form):
    title = forms.CharField(
        label="Titre",
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "readonly": "readonly",
        }),
    )

    template = forms.ModelChoiceField(
        label="Modèle",
        queryset=ProcedureTemplate.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, template_queryset=None, **kwargs):
       super().__init__(*args, **kwargs)
       if template_queryset is None:
           template_queryset = ProcedureTemplate.objects.filter(is_active=True).order_by("title")
       self.fields["template"].queryset = template_queryset


class ProcedureSectionVariablesForm(forms.Form):
    def __init__(self, *args, section=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        self.variable_objects = []

        if section is None:
            return

        for var in section.variables.all().order_by("label", "key"):
            field_name = f"var_{var.key}"
            self.fields[field_name] = forms.CharField(
                label=var.label,
                required=False,
                initial=var.value,
                widget=forms.Textarea(attrs={
                    "class": "form-control",
                    "rows": 2,
                }),
            )
            self.variable_objects.append((field_name, var))

    def save(self):
        for field_name, var in self.variable_objects:
            var.value = self.cleaned_data.get(field_name, "")
            var.save(update_fields=["value"])
