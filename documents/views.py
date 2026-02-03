from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import School, SchoolRole, Procedure

def _schools_for_user(user):
    """
    Écoles accessibles pour l'utilisateur via SchoolRole.users.
    Superuser => toutes les écoles.
    """
    if user.is_superuser:
        return School.objects.all()
    return School.objects.filter(roles__users=user).distinct()


def _role_groups_for_user_in_school(user, school):
    """
    Groups (= rôles) de l'utilisateur DANS une école donnée via SchoolRole.
    """
    if user.is_superuser:
        return Group.objects.all()

    return Group.objects.filter(
        school_roles__school=school,
        school_roles__users=user,
    ).distinct()


@login_required
def school_list(request):
    schools = _schools_for_user(request.user).order_by("name")
    return render(request, "schools/list.html", {"schools": schools})


@login_required
def procedure_list(request):
    """
    Liste des procédures visibles pour l'utilisateur.
    """
    schools = _schools_for_user(request.user)
    procedures = (
        Procedure.objects
        .select_related("school")
        .filter(school__in=schools)
        .order_by("-updated_at")
    )
    return render(request, "procedures/list.html", {"procedures": procedures})

@login_required
def procedure_detail(request, pk):
    schools = _schools_for_user(request.user)
    procedure = get_object_or_404(
        Procedure.objects.select_related("school").filter(school__in=schools),
        pk=pk,
    )

    role_groups = _role_groups_for_user_in_school(request.user, procedure.school)

    sections = (
        procedure.sections
        .prefetch_related("visible_to_groups")
        .filter(
            Q(visible_to_groups__isnull=True) | Q(visible_to_groups__in=role_groups)
        )
        .distinct()
        .order_by("order", "id")
    )

    documents = procedure.documents.all().order_by("-uploaded_at")
    return render(request, "procedures/detail.html", {"procedure": procedure, "sections": sections, "documents": documents})
