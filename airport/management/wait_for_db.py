import os

import psycopg
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        connection = None
        while not connection:
            try:
                connection = psycopg.connect(
                    dbname=os.getenv("POSTGRES_DB"),
                    user=os.getenv("POSTGRES_USER"),
                    password=os.getenv("POSTGRES_PASSWORD"),
                    host=os.getenv("POSTGRES_HOST"),
                    port=os.getenv("POSTGRES_PORT"),
                )
                self.stdout.write(
                    self.style.SUCCESS("Successfully connected to database")
                )
            finally:
                self.stdout.write(self.style.SUCCESS("Database available!"))
