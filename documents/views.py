from django.shortcuts import render
from .models import Document

def document_list(request):
    docs = Document.objects.order_by("-created_at")
    return render(request, "documents/list.html", {"docs": docs})
