from django.contrib import admin

from core.models import AllocationRun, Assignment, Project, Task, Worker


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)


class WorkerAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "capacity_hours")
    list_filter = ("project",)
    search_fields = ("name",)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "priority", "status", "estimated_hours")
    list_filter = ("status", "project")
    search_fields = ("title",)


class AllocationRunAdmin(admin.ModelAdmin):
    list_display = (
        "algorithm",
        "project",
        "total_duration_hours",
        "load_balance_score",
        "completed_tasks_count",
        "created_at",
    )
    list_filter = ("algorithm", "project")


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("task", "worker", "allocation_run", "created_at")
    list_filter = ("allocation_run",)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(AllocationRun, AllocationRunAdmin)
admin.site.register(Assignment, AssignmentAdmin)
