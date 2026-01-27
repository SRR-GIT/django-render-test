from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Procedure

@login_required
def procedure_list(request):
    # MVP: affiche toutes les procédures (on filtrera par établissement ensuite)
    procedures = Procedure.objects.order_by("-updated_at")
    return render(request, "procedures/list.html", {"procedures": procedures})
