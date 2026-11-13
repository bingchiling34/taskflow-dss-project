from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.models import Worker
from core.services import ProjectService, WorkerService


def worker_list(request):
    service = WorkerService()
    project_id = request.GET.get("project")
    selected_project = None
    if project_id:
        selected_project = ProjectService().get_project(project_id)
        workers = service.list_workers(project_id)
    else:
        workers = service.list_workers()

    return render(
        request,
        "workers/list.html",
        {
            "workers": workers,
            "selected_project": selected_project,
            "projects": ProjectService().list_projects(),
        },
    )


@require_http_methods(["GET", "POST"])
def worker_create(request):
    service = WorkerService()
    projects = ProjectService().list_projects()
    default_project_id = request.GET.get("project", "")

    if request.method == "GET":
        return render(
            request,
            "workers/form.html",
            {
                "mode": "create",
                "worker": None,
                "projects": projects,
                "form_data": {
                    "project_id": default_project_id,
                    "name": "",
                    "skills_text": "",
                    "capacity_hours": "40",
                },
                "errors": {},
            },
        )

    form_data = {
        "project_id": request.POST.get("project_id", ""),
        "name": request.POST.get("name", ""),
        "skills_text": request.POST.get("skills_text", ""),
        "capacity_hours": request.POST.get("capacity_hours", "40"),
    }
    worker, errors = service.create_worker(
        form_data["project_id"],
        form_data["name"],
        form_data["skills_text"],
        form_data["capacity_hours"],
    )
    if errors:
        return render(
            request,
            "workers/form.html",
            {
                "mode": "create",
                "worker": None,
                "projects": projects,
                "form_data": form_data,
                "errors": errors,
            },
        )

    messages.success(request, "Worker created.")
    return redirect("worker_detail", worker_id=worker.id)


def worker_detail(request, worker_id):
    worker = get_object_or_404(Worker.objects.select_related("project"), pk=worker_id)
    return render(
        request,
        "workers/detail.html",
        {
            "worker": worker,
            "skills_text": WorkerService().skills_to_text(worker.skills),
        },
    )


@require_http_methods(["GET", "POST"])
def worker_edit(request, worker_id):
    worker = get_object_or_404(Worker.objects.select_related("project"), pk=worker_id)
    service = WorkerService()
    projects = ProjectService().list_projects()

    if request.method == "GET":
        return render(
            request,
            "workers/form.html",
            {
                "mode": "edit",
                "worker": worker,
                "projects": projects,
                "form_data": {
                    "project_id": str(worker.project_id),
                    "name": worker.name,
                    "skills_text": service.skills_to_text(worker.skills),
                    "capacity_hours": str(worker.capacity_hours),
                },
                "errors": {},
            },
        )

    form_data = {
        "project_id": request.POST.get("project_id", ""),
        "name": request.POST.get("name", ""),
        "skills_text": request.POST.get("skills_text", ""),
        "capacity_hours": request.POST.get("capacity_hours", "40"),
    }
    updated, errors = service.update_worker(
        worker,
        form_data["project_id"],
        form_data["name"],
        form_data["skills_text"],
        form_data["capacity_hours"],
    )
    if errors:
        return render(
            request,
            "workers/form.html",
            {
                "mode": "edit",
                "worker": worker,
                "projects": projects,
                "form_data": form_data,
                "errors": errors,
            },
        )

    messages.success(request, "Worker updated.")
    return redirect("worker_detail", worker_id=updated.id)


@require_http_methods(["POST"])
def worker_delete(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    project_id = worker.project_id
    WorkerService().delete_worker(worker)
    messages.success(request, "Worker deleted.")
    return redirect(reverse("worker_list") + "?project=" + str(project_id))
