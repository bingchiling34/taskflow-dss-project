from django.core.management import BaseCommand

from core.services.seed_service import SeedService


class Command(BaseCommand):
    help = "Load demo project, workers, and tasks for allocation demos."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete and recreate the demo project if it already exists.",
        )

    def handle(self, *args, **options):
        result = SeedService().seed(force=options["force"])
        project = result.get("project")

        if result["created"] is False:
            self.stdout.write(self.style.WARNING(result["message"]))
            if project is not None:
                self.stdout.write("Existing project id: " + str(project.id))
            return

        self.stdout.write(self.style.SUCCESS(result["message"]))
        self.stdout.write("Project: " + project.name + " (id=" + str(project.id) + ")")
        self.stdout.write("Workers: " + str(result["worker_count"]))
        self.stdout.write("Tasks: " + str(result["task_count"]))
