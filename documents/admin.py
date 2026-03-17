from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import (
    School,
    SchoolRole,
    ProcedureTemplate,
    ProcedureTemplateSection,
    Procedure,
    ProcedureSection,
    ProcedureDocument,
    ProcedureVersion,
    ProcedureSectionVersion,
    ProcedureTemplateSectionVariable,
    ProcedureSectionVariable,
)
from .services import create_procedure_version

from django.forms import CheckboxSelectMultiple

ROLE_GROUP_NAMES = ["Direction", "Enseignants", "Doyen.ne"]
# -------------------------
# Groupes / permissions
# -------------------------
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "permissions" in self.fields:
            w = self.fields["permissions"].widget
            w.attrs["style"] = "min-height: 260px; width: 100%;"


admin.site.unregister(Group)


@admin.register(Group)
class GroupAdminWithBetterPermissions(GroupAdmin):
    form = GroupAdminForm
    search_fields = ("name",)


# -------------------------
# FORMULAIRES INLINE
# -------------------------
class ProcedureSectionInlineForm(forms.ModelForm):
    class Meta:
        model = ProcedureSection
        fields = "__all__"

    body_html = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={"style": "width: 100%; min-height: 280px;"}),
    )


ROLE_GROUP_NAMES = ["Direction", "Enseignants", "Doyen.ne"]


class ProcedureTemplateSectionInlineForm(forms.ModelForm):
    class Meta:
        model = ProcedureTemplateSection
        fields = "__all__"

    body_html = forms.CharField(
        required=False,
        widget=CKEditorWidget(attrs={"style": "width: 100%; min-height: 240px;"}),
    )

    visible_to_groups = forms.ModelMultipleChoiceField(
        label="Visible par",
        queryset=Group.objects.none(),
        required=False,
        widget=CheckboxSelectMultiple,
        help_text="Si vide : visible pour tous. Sinon : visible uniquement pour ces rôles.",
    )

    editable_by_groups = forms.ModelMultipleChoiceField(
        label="Modifiable par",
        queryset=Group.objects.none(),
        required=False,
        widget=CheckboxSelectMultiple,
        help_text="Si vide : modifiable par tous. Sinon : modifiable uniquement par ces rôles.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        role_qs = Group.objects.filter(name__in=ROLE_GROUP_NAMES).order_by("name")
        self.fields["visible_to_groups"].queryset = role_qs
        self.fields["editable_by_groups"].queryset = role_qs


# -------------------------
# INLINES
# -------------------------
class ProcedureSectionInline(admin.StackedInline):
    model = ProcedureSection
    form = ProcedureSectionInlineForm
    extra = 0
    show_change_link = True
    autocomplete_fields = ("visible_to_groups", "editable_by_groups")

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
        ("Édition", {
            "fields": ("editable_by_groups",),
            "description": "Si vide : modifiable par tous. Sinon : modifiable uniquement par ces rôles.",
        }),
    )


class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0


class ProcedureTemplateSectionInline(admin.StackedInline):
    model = ProcedureTemplateSection
    form = ProcedureTemplateSectionInlineForm
    extra = 0
    show_change_link = True

    fieldsets = (
        (None, {"fields": ("order", "title", "key")}),
        ("Contenu", {"fields": ("body_html",)}),
        ("Visibilité", {"fields": ("visible_to_groups",)}),
        ("Édition", {"fields": ("editable_by_groups",)}),
    )

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        formfield = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name in ["visible_to_groups", "editable_by_groups"]:
            if hasattr(formfield.widget, "can_add_related"):
                formfield.widget.can_add_related = False
            if hasattr(formfield.widget, "can_change_related"):
                formfield.widget.can_change_related = False
            if hasattr(formfield.widget, "can_delete_related"):
                formfield.widget.can_delete_related = False
            if hasattr(formfield.widget, "can_view_related"):
                formfield.widget.can_view_related = False
        return formfield

class SchoolRoleInline(admin.TabularInline):
    model = SchoolRole
    extra = 0
    autocomplete_fields = ("group", "users")


class ProcedureSectionVersionInline(admin.TabularInline):
    model = ProcedureSectionVersion
    extra = 0
    fields = ("order", "title", "key")
    readonly_fields = ("order", "title", "key")
    can_delete = False
    show_change_link = True


class ProcedureVersionInline(admin.TabularInline):
    model = ProcedureVersion
    extra = 0
    fields = ("number", "created_at", "created_by", "comment")
    readonly_fields = ("number", "created_at", "created_by")
    can_delete = False
    show_change_link = True
    ordering = ("-number",)

class ProcedureTemplateSectionVariableInline(admin.TabularInline):
    model = ProcedureTemplateSectionVariable
    extra = 0
    fields = ("key", "label", "default_value")
    
# -------------------------
# ÉTABLISSEMENTS & RÔLES
# -------------------------
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
# MODÈLES DE PROCÉDURE
# -------------------------
@admin.register(ProcedureTemplate)
class ProcedureTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    search_fields = ("title",)
    inlines = [ProcedureTemplateSectionInline]


# -------------------------
# VERSIONS
# -------------------------
@admin.register(ProcedureVersion)
class ProcedureVersionAdmin(admin.ModelAdmin):
    list_display = ("procedure", "number", "created_at", "created_by", "comment")
    list_filter = ("procedure__school",)
    search_fields = ("procedure__title", "procedure__school__name", "comment")
    inlines = [ProcedureSectionVersionInline]
    readonly_fields = ("procedure", "number", "created_at", "created_by")


# -------------------------
# PROCÉDURES
# -------------------------
@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "status", "updated_at")
    list_filter = ("status", "school")
    search_fields = ("title", "school__name")
    autocomplete_fields = ("school", "template", "updated_by")
    inlines = [ProcedureVersionInline]

    class Media:
        css = {"all": ("admin/custom.css",)}

    actions = ["make_snapshot_version"]

    @admin.action(description="Créer une version (snapshot) pour les procédures sélectionnées")
    def make_snapshot_version(self, request, queryset):
        created = 0
        for proc in queryset:
            v = create_procedure_version(proc, user=request.user, comment="Snapshot admin")
            created += 1
        messages.success(request, f"{created} version(s) créée(s).")


# -------------------------
# MASQUER MODÈLES TECHNIQUES
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
    inlines = [ProcedureTemplateSectionVariableInline]

    def has_module_permission(self, request):
        return False
