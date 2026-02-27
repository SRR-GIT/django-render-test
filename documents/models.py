from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group
from ckeditor.fields import RichTextField


class School(models.Model):
    name = models.CharField(max_length=255)
    commune = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"

    def __str__(self):
        return self.name


class SchoolRole(models.Model):
    """
    Assigne des utilisateurs à un rôle (Group) dans une école.
    """
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="roles")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="school_roles")
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="school_roles",
    )

    class Meta:
        unique_together = [("school", "group")]
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

    def __str__(self):
        return f"{self.school} — {self.group.name}"


class ProcedureTemplate(models.Model):
    title = models.CharField(max_length=200, default="Modèle procédure évacuation", verbose_name="Titre")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Modèle de procédure"
        verbose_name_plural = "Modèles de procédure"

    def __str__(self):
        return self.title


class ProcedureTemplateSection(models.Model):
    template = models.ForeignKey(ProcedureTemplate, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=200)
    key = models.SlugField(max_length=80)
    order = models.PositiveIntegerField(default=0)
    body_html = models.TextField(blank=True)

    visible_to_groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="procedure_template_sections",
        help_text="Si vide: visible pour tous. Sinon: visible uniquement pour ces rôles.",
    )

    class Meta:
        ordering = ["order", "id"]
        unique_together = [("template", "key")]
        verbose_name = "Section des modèles de procédures"
        verbose_name_plural = "Sections des modèles de procédures" 

    def __str__(self):
        return f"{self.template}: {self.title}"


class Procedure(models.Model):
    DRAFT = "draft"
    VALIDATED = "validated"
    ARCHIVED = "archived"
    STATUS_CHOICES = [
        (DRAFT, "Brouillon"),
        (VALIDATED, "Validée"),
        (ARCHIVED, "Archivée"),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="procedures")
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    version = models.CharField(max_length=30, blank=True)
    template = models.ForeignKey(ProcedureTemplate, on_delete=models.PROTECT, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Procédure"
        verbose_name_plural = "Procédures"

    def __str__(self):
        return f"{self.school} — {self.title}"


class ProcedureSection(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=200)
    key = models.SlugField(max_length=80)
    order = models.PositiveIntegerField(default=0)
    body_html = RichTextField(
        blank=True,
        help_text="Contenu de la section (texte riche, images, tableaux, etc.)"
    )

    visible_to_groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="procedure_sections",
        help_text="Si vide: visible pour tous. Sinon: visible uniquement pour ces rôles.",
    )

    class Meta:
        verbose_name = "Section (procédure)"
        verbose_name_plural = "Sections (procédures)"
        ordering = ["order", "id"]
        unique_together = [("procedure", "key")]

    def __str__(self):
        return f"{self.procedure}: {self.title}"


class ProcedureDocument(models.Model):
    PLAN = "plan"
    FICHE = "fiche"
    CONSIGNE = "consigne"
    AUTRE = "autre"
    DOC_TYPE_CHOICES = [
        (PLAN, "Plan"),
        (FICHE, "Fiche réflexe"),
        (CONSIGNE, "Consigne"),
        (AUTRE, "Autre"),
    ]

    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="documents")
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default=AUTRE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="procedure_docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProcedureVersion(models.Model):
    procedure = models.ForeignKey("Procedure", on_delete=models.CASCADE, related_name="versions")
    number = models.PositiveIntegerField()  # 1,2,3...
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = [("procedure", "number")]
        ordering = ["-number"]
        verbose_name = "Version des procédures"
        verbose_name_plural = "Versions des procédures"

    def __str__(self):
        return f"{self.procedure} v{self.number}"


class ProcedureSectionVersion(models.Model):
    version = models.ForeignKey(ProcedureVersion, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=200)
    key = models.SlugField(max_length=80)
    order = models.PositiveIntegerField(default=0)
    body_html = models.TextField(blank=True)  # ou RichTextField si tu l’as déjà
    # on “fige” les groupes en snapshot aussi
    visible_to_groups = models.ManyToManyField("auth.Group", blank=True, related_name="procedure_section_versions")

    class Meta:
        ordering = ["order", "id"]
