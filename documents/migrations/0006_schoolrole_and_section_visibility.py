from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0005_merge_0003_0004"),  # adapte si ton dernier merge a un autre numéro
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("school", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="roles", to="documents.school")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="school_roles", to="auth.group")),
            ],
            options={
                "unique_together": {("school", "group")},
            },
        ),
        migrations.AddField(
            model_name="schoolrole",
            name="users",
            field=models.ManyToManyField(blank=True, related_name="school_roles", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="proceduresection",
            name="visible_to_groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="Si vide: visible pour tous. Sinon: visible uniquement pour ces rôles.",
                related_name="procedure_sections",
                to="auth.group",
            ),
        ),
    ]
