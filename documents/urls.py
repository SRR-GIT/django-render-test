from django.urls import path
from .views import procedure_list, procedure_detail

urlpatterns = [
    path("", views.school_list, name="school_list"),
    path("procedures/", views.procedure_list, name="procedure_list"),
    path("procedures/<int:pk>/", views.procedure_detail, name="procedure_detail"),
]

