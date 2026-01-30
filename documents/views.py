from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import School, SchoolRole, Procedure, ProcedureTemplate

def user_groups_for_school(user, school):
    return Group.objects.filter(school_roles__school=school, school_roles__users=user)


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
    schools = (
        School.objects
        .filter(roles__users=request.user)
        .distinct()
        .order_by("name")
    )
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
def template_detail(request, school_id, template_id):
    school = get_object_or_404(School, pk=school_id)
    template = get_object_or_404(ProcedureTemplate, pk=template_id)

    user_groups = _role_groups_for_user_in_school(request.user, school)

    sections = (
        template.sections
        .prefetch_related("visible_to_groups")
        .order_by("order", "id")
    )

    # Filtrage : si visible_to_groups vide => visible à tous
    visible_sections = []
    for s in sections:
        allowed = s.visible_to_groups.all()
        if not allowed.exists() or allowed.filter(id__in=user_groups).exists():
            visible_sections.append(s)

    return render(
        request,
        "templates/detail.html",
        {"school": school, "template": template, "sections": visible_sections},
    )

@login_required
def procedure_detail(request, pk):
    """
    Détail d'une procédure + sections + documents.
    Sécurité: n'autorise que si la procédure appartient à une école accessible.
    Filtrage: sections visibles selon rôles (visible_to_groups)
    """
    schools = _schools_for_user(request.user)

    procedure = get_object_or_404(
        Procedure.objects.select_related("school").filter(school__in=schools),
        pk=pk,
    )

    user_groups = _role_groups_for_user_in_school(request.user, procedure.school)

    # sections/documents
    sections_qs = (
        procedure.sections
        .prefetch_related("visible_to_groups")
        .order_by("order", "id")
    )
    documents = procedure.documents.all().order_by("-uploaded_at")

    # filtre visibilité (si visible_to_groups vide -> visible à tous)
    visible_sections = []
    for s in sections_qs:
        allowed = s.visible_to_groups.all()
        if not allowed.exists() or allowed.filter(id__in=user_groups).exists():
            visible_sections.append(s)

    return render(
        request,
        "procedures/detail.html",
        {
            "procedure": procedure,
            "sections": visible_sections,
            "documents": documents,
        },
    )
