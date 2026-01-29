# documents/migrations/0002_schoolrole_and_visibility.py
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1) On enlève School.groups (présent en DB via 0001, mais plus dans models.py)
        migrations.RemoveField(
            model_name="school",
            name="groups",
        ),

        # 2) On crée SchoolRole
        migrations.CreateModel(
            name="SchoolRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("school", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="roles", to="documents.school")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="school_roles", to="auth.group")),
                ("users", models.ManyToManyField(blank=True, related_name="school_roles", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("school", "group")},
            },
        ),

        # 3) On ajoute visible_to_groups à ProcedureSection
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
