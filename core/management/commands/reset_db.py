from django.core.management import BaseCommand, call_command
from django.db import connection


class Command(BaseCommand):
    help = "Drop public schema tables and recreate via migrations."

    def add_arguments(self, parser):
        parser.add_argument("--noinput", action="store_true")

    def handle(self, *args, **options):
        if options["noinput"] is False:
            confirm = input("This will WIPE the database. Type yes to continue: ")
            if confirm.strip().lower() != "yes":
                self.stdout.write("Aborted.")
                return

        self.stdout.write("Dropping public schema tables...")
        connection.close()

        cursor = connection.cursor()
        sql = """
            DO $$ DECLARE r RECORD;
            BEGIN
              FOR r IN (
                SELECT tablename FROM pg_tables
                WHERE schemaname = 'public'
              ) LOOP
                EXECUTE 'DROP TABLE IF EXISTS public.'
                  || quote_ident(r.tablename) || ' CASCADE';
              END LOOP;
            END $$;
        """
        cursor.execute(sql)
        cursor.close()

        self.stdout.write("Running migrations...")
        call_command("migrate", interactive=False, verbosity=1)
        self.stdout.write("Database reset complete.")
