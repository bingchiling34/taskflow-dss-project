from django.db import models

from .project import Project


class Task(models.Model):
    STATUS_CHOICES = (
        ("todo", "To do"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    required_skills = models.JSONField(default=list, blank=True)
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    priority = models.PositiveSmallIntegerField(default=3)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="todo",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "created_at"]

    def __str__(self):
        return self.title
