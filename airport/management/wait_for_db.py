import os
import time

import psycopg
from django.core.management import BaseCommand
from django.db.utils import OperationalError


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
            except OperationalError:
                self.stdout.write("Database unavailable, trying to connect again...")
                time.sleep(2)

            self.stdout.write(self.style.SUCCESS("Successfully connected to database!"))
