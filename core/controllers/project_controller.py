from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.models import Project
from core.services import ProjectService


def project_list(request):
    projects = ProjectService().list_projects()
    return render(request, "projects/list.html", {"projects": projects})


@require_http_methods(["GET", "POST"])
def project_create(request):
    service = ProjectService()

    if request.method == "GET":
        return render(
            request,
            "projects/form.html",
            {
                "mode": "create",
                "project": None,
                "form_data": {"name": "", "description": "", "status": "active"},
                "errors": {},
            },
        )

    form_data = {
        "name": request.POST.get("name", ""),
        "description": request.POST.get("description", ""),
        "status": request.POST.get("status", "active"),
    }
    project, errors = service.create_project(
        form_data["name"],
        form_data["description"],
        form_data["status"],
    )
    if errors:
        return render(
            request,
            "projects/form.html",
            {
                "mode": "create",
                "project": None,
                "form_data": form_data,
                "errors": errors,
            },
        )

    messages.success(request, "Project created.")
    return redirect("project_detail", project_id=project.id)


def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {
        "project": project,
        "worker_count": project.workers.count(),
        "task_count": project.tasks.count(),
        "allocation_run_count": project.allocation_runs.count(),
    }
    return render(request, "projects/detail.html", context)


@require_http_methods(["GET", "POST"])
def project_edit(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    service = ProjectService()

    if request.method == "GET":
        return render(
            request,
            "projects/form.html",
            {
                "mode": "edit",
                "project": project,
                "form_data": {
                    "name": project.name,
                    "description": project.description,
                    "status": project.status,
                },
                "errors": {},
            },
        )

    form_data = {
        "name": request.POST.get("name", ""),
        "description": request.POST.get("description", ""),
        "status": request.POST.get("status", "active"),
    }
    updated, errors = service.update_project(
        project,
        form_data["name"],
        form_data["description"],
        form_data["status"],
    )
    if errors:
        return render(
            request,
            "projects/form.html",
            {
                "mode": "edit",
                "project": project,
                "form_data": form_data,
                "errors": errors,
            },
        )

    messages.success(request, "Project updated.")
    return redirect("project_detail", project_id=updated.id)


@require_http_methods(["POST"])
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    ProjectService().delete_project(project)
    messages.success(request, "Project deleted.")
    return redirect("project_list")
