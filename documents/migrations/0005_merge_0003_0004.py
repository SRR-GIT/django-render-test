# Generated manually to resolve migration conflict in documents app

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0003_merge_0002_schoolrole_and_visibility_0002_template_section_visibility"),
        ("documents", "0004_richtext_fields"),
    ]

    operations = []
