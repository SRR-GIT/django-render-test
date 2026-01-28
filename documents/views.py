from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Procedure

@login_required
def procedure_list(request):
    # MVP: affiche toutes les procédures (on filtrera par établissement ensuite)
    procedures = Procedure.objects.order_by("-updated_at")
    return render(request, "procedures/list.html", {"procedures": procedures})

from django.shortcuts import get_object_or_404
from .models import Procedure

@login_required
def procedure_detail(request, pk):
    procedure = get_object_or_404(Procedure, pk=pk)
    sections = procedure.sections.all()
    documents = procedure.documents.all()

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
def school_list(request):
    user_groups = request.user.groups.all()
    schools = School.objects.filter(groups__in=user_groups).distinct()
    return render(request, "schools/list.html", {"schools": schools})
