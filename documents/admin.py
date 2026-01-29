from django.contrib import admin
from .models import (
    School,SchoolRole,
    ProcedureTemplate, ProcedureTemplateSection,
    Procedure, ProcedureSection,
    ProcedureDocument,
)

# --- INLINES ---
class ProcedureTemplateSectionInline(admin.TabularInline):
    model = ProcedureTemplateSection
    extra = 0
    filter_horizontal = ("visible_to_groups",)

class ProcedureSectionInline(admin.TabularInline):
    model = ProcedureSection
    extra = 0
    filter_horizontal = ("visible_to_groups",)
    fields = ("order", "title", "key", "body_html", "visible_to_groups")

class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0

class SchoolRoleInline(admin.TabularInline):
    model = SchoolRole
    extra = 0
    filter_horizontal = ("users",)


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


# --- ÉTABLISSEMENTS ---
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "commune", "code")
    search_fields = ("name", "commune", "code")
    filter_horizontal = ("groups",)
    inlines = [SchoolRoleInline]


# --- MODÈLES ---
@admin.register(ProcedureTemplate)
class ProcedureTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    inlines = [ProcedureTemplateSectionInline]


# --- PROCÉDURES ---
@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "status", "updated_at")
    list_filter = ("status", "school")
    search_fields = ("title", "school__name")
    inlines = [ProcedureSectionInline, ProcedureDocumentInline]


'''from django.contrib import admin
from .models import (
    School,
    ProcedureTemplate, ProcedureTemplateSection,
    Procedure, ProcedureSection,
    ProcedureDocument,
)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "commune", "code")
    search_fields = ("name", "commune", "code")
    filter_horizontal = ("groups",)
    
class ProcedureTemplateSectionInline(admin.TabularInline):
    model = ProcedureTemplateSection
    extra = 0

@admin.register(ProcedureTemplate)
class ProcedureTemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    inlines = [ProcedureTemplateSectionInline]

class ProcedureSectionInline(admin.TabularInline):
    model = ProcedureSection
    extra = 0

class ProcedureDocumentInline(admin.TabularInline):
    model = ProcedureDocument
    extra = 0

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("title", "school", "status", "updated_at")
    list_filter = ("status", "school")
    search_fields = ("title", "school__name")
    inlines = [ProcedureSectionInline, ProcedureDocumentInline]

admin.site.register(ProcedureTemplateSection)
admin.site.register(ProcedureSection)
admin.site.register(ProcedureDocument)'''
