from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import School, Procedure


def _schools_for_user(user):
    """
    Retourne les écoles accessibles à l'utilisateur:
    - superuser: toutes
    - sinon: écoles liées aux groupes de l'utilisateur
    """
    if user.is_superuser:
        return School.objects.all().order_by("name")
    return School.objects.filter(groups__user=user).distinct().order_by("name")


@login_required
def school_list(request):
    schools = _schools_for_user(request.user)
    return render(request, "schools/list.html", {"schools": schools})


@login_required
def procedure_list(request):
    """
    Liste des procédures.
    - Optionnel: filtrage par école via ?school=<id>
    - Sécurité: on filtre uniquement sur les écoles accessibles
    """
    schools = _schools_for_user(request.user)

    school_id = request.GET.get("school")
    if school_id:
        school = get_object_or_404(schools, pk=school_id)
        procedures = (
            Procedure.objects.filter(school=school)
            .select_related("school")
            .order_by("-updated_at")
        )
        context = {"procedures": procedures, "school": school, "schools": schools}
        return render(request, "procedures/list.html", context)

    # Sinon: toutes les procédures des écoles accessibles
    procedures = (
        Procedure.objects.filter(school__in=schools)
        .select_related("school")
        .order_by("-updated_at")
    )
    return render(
        request,
        "procedures/list.html",
        {"procedures": procedures, "schools": schools, "school": None},
    )


@login_required
def procedure_detail(request, pk):
    """
    Détail d'une procédure + sections + documents.
    Sécurité: n'autorise que si la procédure appartient à une école accessible.
    """
    schools = _schools_for_user(request.user)

    procedure = get_object_or_404(
        Procedure.objects.select_related("school").filter(school__in=schools),
        pk=pk,
    )

    sections = procedure.sections.all().order_by("order", "id")
    documents = procedure.documents.all().order_by("-uploaded_at")

    return render(
        request,
        "procedures/detail.html",
        {"procedure": procedure, "sections": sections, "documents": documents},
    )
