from django.db import migrations
import ckeditor_uploader.fields

class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0002_..."),  # remplace par la dernière migration existante
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
