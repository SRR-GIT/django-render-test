from django.urls import path
from .views import document_list

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("documents.urls")),
]
