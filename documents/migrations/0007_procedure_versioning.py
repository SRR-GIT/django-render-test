from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0006_schoolrole_and_section_visibility"),  # ⚠️ adapte au dernier fichier chez toi
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcedureVersion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.PositiveIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("comment", models.CharField(blank=True, max_length=255)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ("procedure", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="documents.procedure")),
            ],
            options={
                "ordering": ["-number", "-created_at"],
                "unique_together": {("procedure", "number")},
            },
        ),
        migrations.CreateModel(
            name="ProcedureSectionVersion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("title", models.CharField(max_length=200)),
                ("key", models.SlugField(max_length=80)),
                ("body_html", models.TextField(blank=True)),
                ("version", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sections", to="documents.procedureversion")),
                ("visible_to_groups", models.ManyToManyField(blank=True, related_name="procedure_section_versions", to="auth.group")),
            ],
            options={"ordering": ["order", "id"]},
        ),
    ]
