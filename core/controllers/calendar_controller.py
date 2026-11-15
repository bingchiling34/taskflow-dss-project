from django.shortcuts import render
from django.utils import timezone

from core.services import CalendarService, ProjectService


def calendar_home(request):
    today = timezone.localdate()
    year = request.GET.get("year", today.year)
    month = request.GET.get("month", today.month)
    project_id = request.GET.get("project", "")

    selected_project = None
    if project_id:
        selected_project = ProjectService().get_project(project_id)

    calendar_data = CalendarService().build_month(
        year,
        month,
        project_id if selected_project is not None else None,
    )

    return render(
        request,
        "calendar/home.html",
        {
            "calendar": calendar_data,
            "projects": ProjectService().list_projects(),
            "selected_project": selected_project,
        },
    )
