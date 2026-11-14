from core.models import AllocationRun


class AllocationRunRepository:
    def count(self):
        return AllocationRun.objects.count()

    def list_by_project(self, project_id):
        return list(
            AllocationRun.objects.filter(project_id=project_id)
            .select_related("project")
            .all()
        )

    def list_all(self):
        return list(AllocationRun.objects.select_related("project").all())

    def get_by_id(self, run_id):
        return (
            AllocationRun.objects.filter(pk=run_id)
            .select_related("project")
            .first()
        )

    def create(
        self,
        project,
        algorithm,
        total_duration_hours,
        load_balance_score,
        completed_tasks_count,
        notes="",
    ):
        return AllocationRun.objects.create(
            project=project,
            algorithm=algorithm,
            total_duration_hours=total_duration_hours,
            load_balance_score=load_balance_score,
            completed_tasks_count=completed_tasks_count,
            notes=notes,
        )

    def delete(self, allocation_run):
        allocation_run.delete()
