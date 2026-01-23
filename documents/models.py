from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    category = models.CharField(max_length=100, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
