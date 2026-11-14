from django.shortcuts import render

from core.services import ProjectService
from core.services.analytics_service import AnalyticsService


def analytics_home(request):
    service = AnalyticsService()
    overview = service.get_overview()
    projects = ProjectService().list_projects()
    project_id = request.GET.get("project", "")
    selected_project = None
    comparison = None

    if project_id:
        selected_project = ProjectService().get_project(project_id)
        if selected_project is not None:
            comparison = service.get_project_comparison(project_id)

    context = {
        "projects": projects,
        "selected_project": selected_project,
        "comparison": comparison,
    }
    context["project_count"] = overview["project_count"]
    context["worker_count"] = overview["worker_count"]
    context["task_count"] = overview["task_count"]
    context["allocation_run_count"] = overview["allocation_run_count"]
    return render(request, "analytics/home.html", context)
