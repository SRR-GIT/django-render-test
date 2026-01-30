from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.AddField(
            model_name="proceduretemplatesection",
            name="visible_to_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="procedure_template_sections",
                to="auth.group",
                help_text="Si vide: visible pour tous. Sinon: visible uniquement pour ces rôles.",
            ),
        ),
    ]
