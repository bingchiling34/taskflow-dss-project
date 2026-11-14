from django.shortcuts import render

from core.services import ProjectService
from core.services.analytics_service import AnalyticsService


def analytics_home(request):
    projects = ProjectService().list_projects()
    project_id = request.GET.get("project", "")
    selected_project = None
    comparison = None

    if project_id:
        selected_project = ProjectService().get_project(project_id)
        if selected_project is not None:
            comparison = AnalyticsService().get_project_comparison(project_id)

    return render(
        request,
        "analytics/home.html",
        {
            "projects": projects,
            "selected_project": selected_project,
            "comparison": comparison,
        },
    )
