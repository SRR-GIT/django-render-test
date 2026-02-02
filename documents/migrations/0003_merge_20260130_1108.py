from django.db import migrations
import ckeditor_uploader.fields

class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0002_schoolrole_and_visibility"),
        ("documents", "0002_template_section_visibility"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proceduresection",
            name="body_html",
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name="proceduretemplatesection",
            name="body_html",
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
