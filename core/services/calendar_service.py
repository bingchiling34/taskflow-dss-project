import calendar
from datetime import date

from django.utils import timezone

from core.services.task_service import TaskService


class CalendarService:
    WEEKDAY_LABELS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    def __init__(self):
        self.tasks = TaskService()

    def build_month(self, year, month, project_id=None):
        year, month = self._normalize_month(year, month)
        tasks = self.tasks.list_tasks_with_due_date(project_id)
        by_day = {}

        for task in tasks:
            if task.due_date is None:
                continue
            if task.due_date.year != year:
                continue
            if task.due_date.month != month:
                continue
            day = task.due_date.day
            if day not in by_day:
                by_day[day] = []
            by_day[day].append(task)

        weeks = []
        for week in calendar.monthcalendar(year, month):
            days = []
            for day_number in week:
                if day_number == 0:
                    days.append(
                        {
                            "day": None,
                            "tasks": [],
                            "is_today": False,
                        }
                    )
                else:
                    day_tasks = []
                    if day_number in by_day:
                        day_tasks = by_day[day_number]
                    days.append(
                        {
                            "day": day_number,
                            "tasks": day_tasks,
                            "is_today": self._is_today(year, month, day_number),
                        }
                    )
            weeks.append(days)

        prev_year, prev_month = self._shift_month(year, month, -1)
        next_year, next_month = self._shift_month(year, month, 1)

        return {
            "year": year,
            "month": month,
            "month_label": date(year, month, 1).strftime("%B %Y"),
            "weekday_labels": self.WEEKDAY_LABELS,
            "weeks": weeks,
            "prev_year": prev_year,
            "prev_month": prev_month,
            "next_year": next_year,
            "next_month": next_month,
        }

    def _normalize_month(self, year, month):
        today = timezone.localdate()
        try:
            year_value = int(year)
        except (TypeError, ValueError):
            year_value = today.year
        try:
            month_value = int(month)
        except (TypeError, ValueError):
            month_value = today.month

        if month_value < 1 or month_value > 12:
            month_value = today.month
        if year_value < 2000 or year_value > 2100:
            year_value = today.year
        return year_value, month_value

    def _shift_month(self, year, month, delta):
        month_value = month + delta
        year_value = year
        if month_value < 1:
            month_value = 12
            year_value = year_value - 1
        elif month_value > 12:
            month_value = 1
            year_value = year_value + 1
        return year_value, month_value

    def _is_today(self, year, month, day):
        today = timezone.localdate()
        return today.year == year and today.month == month and today.day == day
