from django.shortcuts import render

from core.services import DashboardService


def home(request):
    overview = DashboardService().get_overview()
    return render(request, "home.html", overview)
