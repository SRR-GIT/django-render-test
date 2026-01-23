import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create a superuser from environment variables if it does not exist."

    def handle(self, *args, **options):
        if os.getenv("AUTO_CREATE_SUPERUSER") != "1":
            self.stdout.write("AUTO_CREATE_SUPERUSER not enabled; skipping.")
            return

        username = os.getenv("ADMIN_USERNAME", "admin")
        email = os.getenv("ADMIN_EMAIL", "s_rossier@Tbluewin.ch")
        password = os.getenv("ADMIN_PASSWORD")

        if not password:
            raise SystemExit("ADMIN_PASSWORD is required when AUTO_CREATE_SUPERUSER=1")

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superuser '{username}' already exists; skipping.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f"Superuser '{username}' created.")
