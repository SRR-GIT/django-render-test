from django.db import transaction
from django.db.models import Max
from .models import ProcedureVersion, ProcedureSectionVersion, Procedure, ProcedureSection

@transaction.atomic
def create_procedure_version(procedure, user=None, comment=""):
    last = procedure.versions.aggregate(m=Max("number"))["m"] or 0
    v = ProcedureVersion.objects.create(
        procedure=procedure,
        number=last + 1,
        created_by=user,
        comment=comment,
    )

    # snapshot des sections courantes
    for s in procedure.sections.prefetch_related("visible_to_groups").all().order_by("order", "id"):
        sv = ProcedureSectionVersion.objects.create(
            version=v,
            title=s.title,
            key=s.key,
            order=s.order,
            body_html=s.body_html,
        )
        sv.visible_to_groups.set(s.visible_to_groups.all())

    return v
    
def create_procedure_from_template(*, school, template, title, user):
    proc = Procedure.objects.create(
        school=school,
        template=template,
        title=title,
        status=Procedure.DRAFT,
        updated_by=user,
    )

    # Copier les sections du modèle
    for ts in template.sections.all().order_by("order", "id"):
        ps = ProcedureSection.objects.create(
            procedure=proc,
            title=ts.title,
            key=ts.key,
            order=ts.order,
            body_html=ts.body_html,
        )
        # copier les droits
        ps.visible_to_groups.set(ts.visible_to_groups.all())
        ps.editable_by_groups.set(ts.editable_by_groups.all())

    return proc
