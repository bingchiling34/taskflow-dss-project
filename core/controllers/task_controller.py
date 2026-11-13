from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.models import Task
from core.services import ProjectService, TaskService


def task_list(request):
    service = TaskService()
    project_id = request.GET.get("project")
    selected_project = None
    if project_id:
        selected_project = ProjectService().get_project(project_id)
        tasks = service.list_tasks(project_id)
    else:
        tasks = service.list_tasks()

    return render(
        request,
        "tasks/list.html",
        {
            "tasks": tasks,
            "selected_project": selected_project,
            "projects": ProjectService().list_projects(),
        },
    )


@require_http_methods(["GET", "POST"])
def task_create(request):
    service = TaskService()
    projects = ProjectService().list_projects()
    default_project_id = request.GET.get("project", "")

    if request.method == "GET":
        return render(
            request,
            "tasks/form.html",
            {
                "mode": "create",
                "task": None,
                "projects": projects,
                "form_data": {
                    "project_id": default_project_id,
                    "title": "",
                    "description": "",
                    "skills_text": "",
                    "estimated_hours": "1",
                    "priority": "3",
                    "status": "todo",
                },
                "errors": {},
            },
        )

    form_data = {
        "project_id": request.POST.get("project_id", ""),
        "title": request.POST.get("title", ""),
        "description": request.POST.get("description", ""),
        "skills_text": request.POST.get("skills_text", ""),
        "estimated_hours": request.POST.get("estimated_hours", "1"),
        "priority": request.POST.get("priority", "3"),
        "status": request.POST.get("status", "todo"),
    }
    task, errors = service.create_task(
        form_data["project_id"],
        form_data["title"],
        form_data["description"],
        form_data["skills_text"],
        form_data["estimated_hours"],
        form_data["priority"],
        form_data["status"],
    )
    if errors:
        return render(
            request,
            "tasks/form.html",
            {
                "mode": "create",
                "task": None,
                "projects": projects,
                "form_data": form_data,
                "errors": errors,
            },
        )

    messages.success(request, "Task created.")
    return redirect("task_detail", task_id=task.id)


def task_detail(request, task_id):
    task = get_object_or_404(Task.objects.select_related("project"), pk=task_id)
    return render(
        request,
        "tasks/detail.html",
        {
            "task": task,
            "skills_text": TaskService().skills_to_text(task.required_skills),
        },
    )


@require_http_methods(["GET", "POST"])
def task_edit(request, task_id):
    task = get_object_or_404(Task.objects.select_related("project"), pk=task_id)
    service = TaskService()
    projects = ProjectService().list_projects()

    if request.method == "GET":
        return render(
            request,
            "tasks/form.html",
            {
                "mode": "edit",
                "task": task,
                "projects": projects,
                "form_data": {
                    "project_id": str(task.project_id),
                    "title": task.title,
                    "description": task.description,
                    "skills_text": service.skills_to_text(task.required_skills),
                    "estimated_hours": str(task.estimated_hours),
                    "priority": str(task.priority),
                    "status": task.status,
                },
                "errors": {},
            },
        )

    form_data = {
        "project_id": request.POST.get("project_id", ""),
        "title": request.POST.get("title", ""),
        "description": request.POST.get("description", ""),
        "skills_text": request.POST.get("skills_text", ""),
        "estimated_hours": request.POST.get("estimated_hours", "1"),
        "priority": request.POST.get("priority", "3"),
        "status": request.POST.get("status", "todo"),
    }
    updated, errors = service.update_task(
        task,
        form_data["project_id"],
        form_data["title"],
        form_data["description"],
        form_data["skills_text"],
        form_data["estimated_hours"],
        form_data["priority"],
        form_data["status"],
    )
    if errors:
        return render(
            request,
            "tasks/form.html",
            {
                "mode": "edit",
                "task": task,
                "projects": projects,
                "form_data": form_data,
                "errors": errors,
            },
        )

    messages.success(request, "Task updated.")
    return redirect("task_detail", task_id=updated.id)


@require_http_methods(["POST"])
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project_id = task.project_id
    TaskService().delete_task(task)
    messages.success(request, "Task deleted.")
    return redirect(reverse("task_list") + "?project=" + str(project_id))
