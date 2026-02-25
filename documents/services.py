from django.db import transaction
from django.db.models import Max
from .models import ProcedureVersion, ProcedureSectionVersion

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
