# Generated manually (Option B) - initial migration for documents app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # Group table lives in auth app
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcedureTemplate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(default="Modèle procédure évacuation", max_length=200)),
                ("is_active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("commune", models.CharField(blank=True, max_length=255)),
                ("code", models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="ProcedureTemplateSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("key", models.SlugField(max_length=80)),
                ("order", models.PositiveIntegerField(default=0)),
                ("body_html", models.TextField(blank=True)),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="documents.proceduretemplate",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "id"],
                "unique_together": {("template", "key")},
            },
        ),
        migrations.CreateModel(
            name="Procedure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("status", models.CharField(choices=[("draft", "Brouillon"), ("validated", "Validée"), ("archived", "Archivée")], default="draft", max_length=20)),
                ("version", models.CharField(blank=True, max_length=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="procedures",
                        to="documents.school",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="documents.proceduretemplate",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProcedureSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("key", models.SlugField(max_length=80)),
                ("order", models.PositiveIntegerField(default=0)),
                ("body_html", models.TextField(blank=True)),
                (
                    "procedure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="documents.procedure",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "id"],
                "unique_together": {("procedure", "key")},
            },
        ),
        migrations.CreateModel(
            name="ProcedureDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("doc_type", models.CharField(choices=[("plan", "Plan"), ("fiche", "Fiche réflexe"), ("consigne", "Consigne"), ("autre", "Autre")], default="autre", max_length=20)),
                ("title", models.CharField(max_length=200)),
                ("file", models.FileField(upload_to="procedure_docs/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "procedure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="documents.procedure",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="school",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="Groupes autorisés à accéder à cette école",
                related_name="schools",
                to="auth.group",
            ),
        ),
    ]
