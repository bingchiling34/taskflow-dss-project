from core.models import Assignment


class AssignmentRepository:
    def create_many(self, allocation_run, pairs):
        rows = []
        for task, worker in pairs:
            rows.append(
                Assignment(
                    allocation_run=allocation_run,
                    task=task,
                    worker=worker,
                )
            )
        return Assignment.objects.bulk_create(rows)

    def list_by_run(self, allocation_run_id):
        return list(
            Assignment.objects.filter(allocation_run_id=allocation_run_id)
            .select_related("task", "worker")
            .all()
        )
