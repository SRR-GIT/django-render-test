from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0009_add_editable_by_groups_to_proceduresection"),  # adapte au vrai dernier nom
    ]

    operations = [
        migrations.CreateModel(
            name="ProcedureTemplateSectionVariable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=100)),
                ("label", models.CharField(max_length=200)),
                ("default_value", models.TextField(blank=True)),
                (
                    "template_section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variables",
                        to="documents.proceduretemplatesection",
                    ),
                ),
            ],
            options={
                "unique_together": {("template_section", "key")},
                "verbose_name": "Variable (modèle)",
                "verbose_name_plural": "Variables (modèle)",
            },
        ),
        migrations.CreateModel(
            name="ProcedureSectionVariable",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.SlugField(max_length=100)),
                ("label", models.CharField(max_length=200)),
                ("value", models.TextField(blank=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variables",
                        to="documents.proceduresection",
                    ),
                ),
            ],
            options={
                "unique_together": {("section", "key")},
                "verbose_name": "Variable (procédure)",
                "verbose_name_plural": "Variables (procédure)",
            },
        ),
    ]
