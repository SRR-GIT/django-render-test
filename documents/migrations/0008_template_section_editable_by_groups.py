from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("documents", "0007_procedure_versioning.py"),
    ]

    operations = [
        migrations.AddField(
            model_name="proceduretemplatesection",
            name="editable_by_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="procedure_template_sections_editable",
                to="auth.group",
                help_text="Si vide: modifiable par tous les rôles. Sinon: modifiable uniquement par ces rôles.",
            ),
        ),
    ]
