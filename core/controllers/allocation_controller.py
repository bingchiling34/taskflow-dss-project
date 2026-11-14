from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.models import AllocationRun
from core.services import AllocationService, ProjectService
from core.services.algorithms import ALGORITHM_CHOICES


def _algorithm_label(key):
    for item_key, label in ALGORITHM_CHOICES:
        if item_key == key:
            return label
    return key


def allocation_home(request):
    service = AllocationService()
    projects = ProjectService().list_projects()
    project_id = request.GET.get("project", "")
    selected_project = None
    run_rows = []

    if project_id:
        selected_project = ProjectService().get_project(project_id)
        if selected_project is not None:
            runs = service.list_runs(project_id)
            for run in runs:
                run_rows.append(
                    {
                        "run": run,
                        "label": _algorithm_label(run.algorithm),
                    }
                )

    return render(
        request,
        "allocation/home.html",
        {
            "projects": projects,
            "selected_project": selected_project,
            "algorithms": ALGORITHM_CHOICES,
            "run_rows": run_rows,
        },
    )


@require_http_methods(["POST"])
def allocation_run(request):
    service = AllocationService()
    project_id = request.POST.get("project_id", "")
    mode = request.POST.get("mode", "one")
    algorithm = request.POST.get("algorithm", "")

    back_url = reverse("allocation_home")
    if project_id:
        back_url = back_url + "?project=" + str(project_id)

    if mode == "all":
        created, errors = service.run_all_algorithms(project_id)
        if errors and not created:
            for key, value in errors.items():
                messages.error(request, key + ": " + str(value))
            return redirect(back_url)
        messages.success(
            request,
            "Created " + str(len(created)) + " allocation runs.",
        )
        return redirect(back_url)

    run, errors = service.run_algorithm(project_id, algorithm)
    if errors:
        for value in errors.values():
            messages.error(request, value)
        return redirect(back_url)

    messages.success(request, "Allocation run created.")
    return redirect("allocation_run_detail", run_id=run.id)


def allocation_run_detail(request, run_id):
    service = AllocationService()
    run = get_object_or_404(AllocationRun.objects.select_related("project"), pk=run_id)
    assignments = service.get_run_assignments(run_id)
    return render(
        request,
        "allocation/detail.html",
        {
            "run": run,
            "assignments": assignments,
            "algorithm_label": _algorithm_label(run.algorithm),
        },
    )


@require_http_methods(["POST"])
def allocation_run_delete(request, run_id):
    run = get_object_or_404(AllocationRun, pk=run_id)
    project_id = run.project_id
    AllocationService().delete_run(run)
    messages.success(request, "Allocation run deleted.")
    return redirect(reverse("allocation_home") + "?project=" + str(project_id))
