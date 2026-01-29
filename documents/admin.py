from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    School,SchoolRole,
    ProcedureTemplate, 
    ProcedureTemplateSection,
    Procedure, 
    ProcedureSection,
    ProcedureDocument,
)

# --- INLINES ---
class ProcedureTemplateSectionInline(admin.TabularInline):
    model = ProcedureTemplateSection
    extra = 0

class ProcedureSectionInline(admin.TabularInline):
    model = ProcedureSection
    extra = 0
    filter_horizontal = ("visible_to_groups",)
    fields = ("order", "title", "key", "body_html", "visible_to_groups")

class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0


# --- MASQUER LES MODÈLES TECHNIQUES DU MENU ---
@admin.register(ProcedureTemplateSection)
class ProcedureTemplateSectionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(ProcedureSection)
class ProcedureSectionAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(ProcedureDocument)
class ProcedureDocumentAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

# -------------------------
# Rôles par établissement
# -------------------------

class SchoolRoleInline(admin.TabularInline):
    model = SchoolRole
    extra = 0
    autocomplete_fields = ("group", "users")  # nécessite search_fields sur User admin
    # pour ManyToManyField "users"
    filter_horizontal = ("users",)


@admin.register(SchoolRole)
class SchoolRoleAdmin(admin.ModelAdmin):
    list_display = ("school", "group")
    list_filter = ("group", "school")
    search_fields = ("school__name", "group__name", "users__username", "users__email")
    filter_horizontal = ("users",)
    autocomplete_fields = ("school", "group")



# --- ÉTABLISSEMENTS ---
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "commune", "code")
    search_fields = ("name", "commune", "code")
    inlines = [SchoolRoleInline]
    #filter_horizontal = ("groups",)
    #inlines = [SchoolRoleInline]


# -------------------------
# Modèles de procédure
# -------------------------

class ProcedureTemplateSectionInline(admin.TabularInline):
    model = ProcedureTemplateSection
    extra = 0


@admin.register(ProcedureTemplate)
class ProcedureTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    inlines = [ProcedureTemplateSectionInline]


@admin.register(ProcedureTemplateSection)
class ProcedureTemplateSectionAdmin(admin.ModelAdmin):
    list_display = ("template", "order", "title", "key")
    list_filter = ("template",)
    search_fields = ("title", "key", "template__title")
    ordering = ("template", "order", "id")



# -------------------------
# Procédures + sections + docs
# -------------------------

class ProcedureSectionInline(admin.TabularInline):
    model = ProcedureSection
    extra = 0
    # pour ManyToMany visible_to_groups sur ProcedureSection
    filter_horizontal = ("visible_to_groups",)


class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "status", "updated_at")
    list_filter = ("status", "school")
    search_fields = ("title", "school__name")
    inlines = [ProcedureSectionInline, ProcedureDocumentInline]


@admin.register(ProcedureSection)
class ProcedureSectionAdmin(admin.ModelAdmin):
    list_display = ("procedure", "order", "title", "key")
    list_filter = ("procedure__school",)
    search_fields = ("title", "key", "procedure__title", "procedure__school__name")
    ordering = ("procedure", "order", "id")
    filter_horizontal = ("visible_to_groups",)


@admin.register(ProcedureDocument)
class ProcedureDocumentAdmin(admin.ModelAdmin):
    list_display = ("procedure", "doc_type", "title", "uploaded_at")
    list_filter = ("doc_type", "procedure__school")
    search_fields = ("title", "procedure__title", "procedure__school__name")
    
