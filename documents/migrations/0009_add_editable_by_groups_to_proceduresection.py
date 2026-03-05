from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0008_template_section_editable_by_groups"),  # <-- remplace par ta dernière migration
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="proceduresection",
            name="editable_by_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="procedure_sections_editable",
                to="auth.group",
                help_text="Si vide: modifiable par tous les rôles. Sinon: modifiable uniquement par ces rôles.",
            ),
        ),
    ]
