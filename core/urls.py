from django.urls import path

from core.controllers import (
    home,
    project_create,
    project_delete,
    project_detail,
    project_edit,
    project_list,
)

urlpatterns = [
    path("", home, name="home"),
    path("projects/", project_list, name="project_list"),
    path("projects/new/", project_create, name="project_create"),
    path("projects/<int:project_id>/", project_detail, name="project_detail"),
    path("projects/<int:project_id>/edit/", project_edit, name="project_edit"),
    path("projects/<int:project_id>/delete/", project_delete, name="project_delete"),
]
