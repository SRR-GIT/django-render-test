from django.urls import path
from .views import procedure_list

urlpatterns = [
    path("", procedure_list, name="procedure_list"),
    path("<int:pk>/", procedure_detail, name="procedure_detail"),
]

