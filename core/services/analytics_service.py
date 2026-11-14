from core.repositories import AllocationRunRepository, ProjectRepository
from core.services.algorithms import ALGORITHM_CHOICES


class AnalyticsService:
    def __init__(self):
        self.projects = ProjectRepository()
        self.runs = AllocationRunRepository()

    def get_project_comparison(self, project_id):
        project = self.projects.get_by_id(project_id)
        if project is None:
            return None

        runs = self.runs.list_by_project(project_id)
        latest_by_algorithm = {}
        for run in runs:
            if run.algorithm not in latest_by_algorithm:
                latest_by_algorithm[run.algorithm] = run

        rows = []
        for key, label in ALGORITHM_CHOICES:
            if key not in latest_by_algorithm:
                continue
            run = latest_by_algorithm[key]
            rows.append(
                {
                    "algorithm_key": key,
                    "algorithm_label": label,
                    "run": run,
                    "duration": run.total_duration_hours,
                    "load_balance": run.load_balance_score,
                    "assigned_tasks": run.completed_tasks_count,
                }
            )

        best_duration = self._find_best_duration(rows)
        best_balance = self._find_best_balance(rows)

        chart_labels = []
        chart_durations = []
        chart_balances = []
        chart_assigned = []
        for row in rows:
            chart_labels.append(row["algorithm_label"])
            chart_durations.append(float(row["duration"] or 0))
            chart_balances.append(float(row["load_balance"] or 0))
            chart_assigned.append(row["assigned_tasks"])

        return {
            "project": project,
            "rows": rows,
            "best_duration": best_duration,
            "best_balance": best_balance,
            "chart_labels": chart_labels,
            "chart_durations": chart_durations,
            "chart_balances": chart_balances,
            "chart_assigned": chart_assigned,
            "has_data": len(rows) > 0,
        }

    def _find_best_duration(self, rows):
        best = None
        for row in rows:
            if row["duration"] is None:
                continue
            if best is None:
                best = row
                continue
            if row["duration"] < best["duration"]:
                best = row
        return best

    def _find_best_balance(self, rows):
        best = None
        for row in rows:
            if row["load_balance"] is None:
                continue
            if best is None:
                best = row
                continue
            if row["load_balance"] < best["load_balance"]:
                best = row
        return best
