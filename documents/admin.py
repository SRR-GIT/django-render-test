from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib import admin

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdminWithSearch(GroupAdmin):
    search_fields = ("name",)


from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

from .models import (
    School, SchoolRole,
    ProcedureTemplate, ProcedureTemplateSection,
    Procedure, ProcedureSection, ProcedureDocument,
)

# -------------------------
# FORM POUR L'INLINE
# -------------------------
class ProcedureSectionInlineForm(forms.ModelForm):
    class Meta:
        model = ProcedureSection
        fields = "__all__"

    # Force un widget CKEditor plus grand (même en inline)
    body_html = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={"style": "width: 100%; min-height: 280px;"}),
    )


# -------------------------
# INLINES
# -------------------------
class ProcedureSectionInline(admin.StackedInline):  # <- IMPORTANT : StackedInline
    model = ProcedureSection
    form = ProcedureSectionInlineForm
    extra = 0
    show_change_link = True

    # Autocomplete (compact) au lieu de filter_horizontal (énorme)
    autocomplete_fields = ("visible_to_groups",)

    fieldsets = (
        (None, {
            "fields": ("order", "title", "key"),
        }),
        ("Contenu", {
            "fields": ("body_html",),
        }),
        ("Visibilité", {
            "fields": ("visible_to_groups",),
            "description": "Si vide : visible pour tous. Sinon : visible uniquement pour ces rôles.",
        }),
    )


class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0


class ProcedureTemplateSectionInlineForm(forms.ModelForm):
    class Meta:
        model = ProcedureTemplateSection
        fields = "__all__"

    body_html = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={"style": "width: 100%; min-height: 240px;"}),
    )


class ProcedureTemplateSectionInline(admin.StackedInline):
    model = ProcedureTemplateSection
    form = ProcedureTemplateSectionInlineForm
    extra = 0
    show_change_link = True
    # si tu ajoutes visible_to_groups plus tard sur template section :
    # autocomplete_fields = ("visible_to_groups",)


# -------------------------
# MASQUER MODÈLES TECHNIQUES (optionnel)
# -------------------------
@admin.register(ProcedureSection)
class ProcedureSectionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(ProcedureDocument)
class ProcedureDocumentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(ProcedureTemplateSection)
class ProcedureTemplateSectionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


# -------------------------
# ÉTABLISSEMENTS & RÔLES
# -------------------------
class SchoolRoleInline(admin.TabularInline):
    model = SchoolRole
    extra = 0
    autocomplete_fields = ("group", "users")


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "commune", "code")
    search_fields = ("name", "commune", "code")
    inlines = [SchoolRoleInline]


@admin.register(SchoolRole)
class SchoolRoleAdmin(admin.ModelAdmin):
    list_display = ("school", "group")
    list_filter = ("group", "school")
    search_fields = ("school__name", "group__name", "users__username", "users__email")
    autocomplete_fields = ("school", "group", "users")


# -------------------------
# PROCÉDURES
# -------------------------
@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "status", "updated_at")
    list_filter = ("status", "school")
    search_fields = ("title", "school__name")
    autocomplete_fields = ("school", "template", "updated_by")
    inlines = [ProcedureSectionInline, ProcedureDocumentInline]
    class Media:
        css = {"all": ("admin/custom.css",)}


# -------------------------
# MODÈLES DE PROCÉDURE
# -------------------------
@admin.register(ProcedureTemplate)
class ProcedureTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    inlines = [ProcedureTemplateSectionInline]
