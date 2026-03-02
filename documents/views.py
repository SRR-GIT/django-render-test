from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .forms import ProcedureCreateForm
from .services import create_procedure_from_template
from .models import School

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

def _is_director_in_school(user, school) -> bool:
    if user.is_superuser:
        return True
    return school.roles.filter(group__name="Direction", users=user).exists()

@login_required
def procedure_create(request, school_id):
    school = School.objects.get(pk=school_id)

    if not _is_director_in_school(request.user, school):
        return HttpResponseForbidden("Accès réservé au rôle Direction pour cet établissement.")

    if request.method == "POST":
        form = ProcedureCreateForm(request.POST)
        if form.is_valid():
            proc = create_procedure_from_template(
                school=school,
                template=form.cleaned_data["template"],
                title=form.cleaned_data["title"],
                user=request.user,
            )
            return redirect("procedure_detail", pk=proc.pk)
    else:
        form = ProcedureCreateForm()

    return render(request, "procedures/create.html", {"school": school, "form": form})

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import ProcedureSectionEditForm
from .models import ProcedureSection

@login_required
def procedure_section_edit(request, section_id):
    section = get_object_or_404(
        ProcedureSection.objects
        .select_related("procedure__school")
        .prefetch_related("editable_by_groups"),
        pk=section_id,
    )

    school = section.procedure.school

    role_groups = _role_groups_for_user_in_school(request.user, school)

    allowed = (
        section.editable_by_groups.count() == 0
        or section.editable_by_groups.filter(
            id__in=role_groups.values_list("id", flat=True)
        ).exists()
    )

    if not allowed and not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette section.")

    if request.method == "POST":
        form = ProcedureSectionEditForm(request.POST, instance=section)
        if form.is_valid():
            s = form.save(commit=False)
            s.procedure.updated_by = request.user
            s.procedure.save(update_fields=["updated_by", "updated_at"])
            s.save()
            return redirect("procedure_detail", pk=section.procedure_id)
    else:
        form = ProcedureSectionEditForm(instance=section)

    return render(request, "procedures/section_edit.html", {
        "section": section,
        "form": form,
    })
