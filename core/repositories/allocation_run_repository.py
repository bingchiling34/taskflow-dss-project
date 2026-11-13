from core.models import AllocationRun


class AllocationRunRepository:
    def count(self):
        return AllocationRun.objects.count()
