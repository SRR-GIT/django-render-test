from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0010_section_variable"),
    ]

    operations = [
        migrations.CreateModel(
            name="GlobalVariable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "key",
                    models.CharField(
                        help_text="Exemple : numero_cantonal",
                        max_length=100,
                        unique=True,
                        verbose_name="Clé",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        max_length=255,
                        verbose_name="Libellé",
                    ),
                ),
                (
                    "value",
                    models.TextField(
                        blank=True,
                        verbose_name="Valeur",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="Dernière modification",
                    ),
                ),
            ],
            options={
                "verbose_name": "Variable globale",
                "verbose_name_plural": "Variables globales",
                "ordering": ["label"],
            },
        ),
    ]
