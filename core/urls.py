from django.urls import path

from core.controllers import (
    home,
    project_create,
    project_delete,
    project_detail,
    project_edit,
    project_list,
    worker_create,
    worker_delete,
    worker_detail,
    worker_edit,
    worker_list,
)

urlpatterns = [
    path("", home, name="home"),
    path("projects/", project_list, name="project_list"),
    path("projects/new/", project_create, name="project_create"),
    path("projects/<int:project_id>/", project_detail, name="project_detail"),
    path("projects/<int:project_id>/edit/", project_edit, name="project_edit"),
    path("projects/<int:project_id>/delete/", project_delete, name="project_delete"),
    path("workers/", worker_list, name="worker_list"),
    path("workers/new/", worker_create, name="worker_create"),
    path("workers/<int:worker_id>/", worker_detail, name="worker_detail"),
    path("workers/<int:worker_id>/edit/", worker_edit, name="worker_edit"),
    path("workers/<int:worker_id>/delete/", worker_delete, name="worker_delete"),
]
