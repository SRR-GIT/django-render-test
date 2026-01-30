from django.contrib import admin
from .models import (
    School,
    SchoolRole,
    ProcedureTemplate,
    ProcedureTemplateSection,
    Procedure,
    ProcedureSection,
    ProcedureDocument,
)

# -------------------------
# Rôles par établissement
# -------------------------

class SchoolRoleInline(admin.TabularInline):
    model = SchoolRole
    extra = 0
    autocomplete_fields = ("group", "users")
    filter_horizontal = ("users",)


@admin.register(SchoolRole)
class SchoolRoleAdmin(admin.ModelAdmin):
    list_display = ("school", "group")
    list_filter = ("group", "school")
    search_fields = ("school__name", "group__name", "users__username", "users__email")
    filter_horizontal = ("users",)
    autocomplete_fields = ("school", "group")


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "commune", "code")
    search_fields = ("name", "commune", "code")
    inlines = [SchoolRoleInline]


# -------------------------
# Modèles de procédure
# -------------------------

class ProcedureTemplateSectionInline(admin.TabularInline):
    model = ProcedureTemplateSection
    extra = 0
    filter_horizontal = ("visible_to_groups",)
    fields = ("order", "title", "key", "body_html", "visible_to_groups")



@admin.register(ProcedureTemplate)
class ProcedureTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    inlines = [ProcedureTemplateSectionInline]


# -------------------------
# Procédures + sections + docs
# -------------------------

class ProcedureSectionInline(admin.TabularInline):
    model = ProcedureSection
    extra = 0
    filter_horizontal = ("visible_to_groups",)
    fields = ("order", "title", "key", "body_html", "visible_to_groups")


class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "status", "updated_at")
    list_filter = ("status", "school")
    search_fields = ("title", "school__name")
    inlines = [ProcedureSectionInline, ProcedureDocumentInline]


# -------------------------
# Cacher les modèles techniques du menu
# (mais ils restent accessibles via les inlines)
# -------------------------

@admin.register(ProcedureTemplateSection)
class ProcedureTemplateSectionHiddenAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(ProcedureSection)
class ProcedureSectionHiddenAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(ProcedureDocument)
class ProcedureDocumentHiddenAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
