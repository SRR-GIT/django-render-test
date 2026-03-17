import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProcedureCreateForm, ProcedureSectionEditForm
from .models import School, SchoolRole, Procedure, ProcedureSection, ProcedureTemplate


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
    Groupes (= rôles) de l'utilisateur DANS une école donnée via SchoolRole.
    """
    if user.is_superuser:
        return Group.objects.all()

    return Group.objects.filter(
        school_roles__school=school,
        school_roles__users=user,
    ).distinct()


def _is_director_in_school(user, school) -> bool:
    """
    L'utilisateur est directeur s'il appartient au groupe 'Direction'
    dans cette école (via SchoolRole).
    """
    if user.is_superuser:
        return True

    return SchoolRole.objects.filter(
        school=school,
        group__name="Direction",
        users=user,
    ).exists()


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
    role_group_ids = set(role_groups.values_list("id", flat=True))

    sections_qs = (
        procedure.sections
        .prefetch_related("visible_to_groups", "editable_by_groups", "variables")
        .filter(
            Q(visible_to_groups__isnull=True) | Q(visible_to_groups__in=role_groups)
        )
        .distinct()
        .order_by("order", "id")
    )

    sections = []
    for section in sections_qs:
        editable_group_ids = set(section.editable_by_groups.values_list("id", flat=True))
        section.can_edit = (
            request.user.is_superuser
            or bool(editable_group_ids & role_group_ids)
        )

        rendered_html = section.body_html or ""

        variables_map = {
            var.key: (var.value or "")
            for var in section.variables.all()
        }

        for key, value in variables_map.items():
            rendered_html = re.sub(
                rf"{{{{\s*{re.escape(key)}\s*}}}}",
                value,
                rendered_html,
            )

        section.rendered_html = rendered_html
        sections.append(section)

    documents = procedure.documents.all().order_by("-uploaded_at")

    return render(
        request,
        "procedures/detail.html",
        {
            "procedure": procedure,
            "sections": sections,
            "documents": documents,
        },
    )

@login_required
def procedure_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)

    if not _schools_for_user(request.user).filter(pk=school.pk).exists():
        return HttpResponseForbidden("Accès refusé à cet établissement.")

    if not _is_director_in_school(request.user, school):
        return HttpResponseForbidden("Seuls les directeurs peuvent créer une procédure.")

    if request.method == "POST":
        form = ProcedureCreateForm(request.POST)
        if form.is_valid():
            template = form.cleaned_data["template"]

            proc = Procedure.objects.create(
                school=school,
                title=template.title,
                template=template,
                status=Procedure.DRAFT,
                updated_by=request.user,
            )

            template_sections = (
                template.sections
                .prefetch_related("visible_to_groups", "editable_by_groups")
                .order_by("order", "id")
            )

            for ts in template_sections:
                ps = ProcedureSection.objects.create(
                    procedure=proc,
                    title=ts.title,
                    key=ts.key,
                    order=ts.order,
                    body_html=ts.body_html,
                )
                ps.visible_to_groups.set(ts.visible_to_groups.all())
                ps.editable_by_groups.set(ts.editable_by_groups.all())

                for var in ts.variables.all():
                    ProcedureSectionVariable.objects.create(
                        section=ps,
                        key=var.key,
                        label=var.label,
                        value=var.default_value,
                    )
            return redirect("procedure_detail", pk=proc.pk)
    else:
        form = ProcedureCreateForm()

    return render(
        request,
        "procedures/create.html",
        {
            "school": school,
            "form": form,
        },
    )


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
    role_group_ids = role_groups.values_list("id", flat=True)

    allowed = (
        request.user.is_superuser
        or section.editable_by_groups.filter(id__in=role_group_ids).exists()
    )

    if not allowed:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette section.")

    if request.method == "POST":
        form = ProcedureSectionEditForm(request.POST, instance=section)
        if form.is_valid():
            edited_section = form.save(commit=False)
            edited_section.save()

            procedure = section.procedure
            procedure.updated_by = request.user
            procedure.save(update_fields=["updated_by", "updated_at"])

            return redirect("procedure_detail", pk=section.procedure_id)
    else:
        form = ProcedureSectionEditForm(instance=section)

    return render(
        request,
        "procedures/section_edit.html",
        {
            "section": section,
            "form": form,
        },
    )
