from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Message

class Command(BaseCommand):
    help = 'Fix Message.user field to reference User objects'

    def handle(self, *args, **kwargs):
        for msg in Message.objects.all():
            try:
                user = User.objects.get(username=msg.user)
                msg.user = user
                msg.save()
                self.stdout.write(self.style.SUCCESS(f"Updated message ID {msg.id}"))
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"User '{msg.user}' does not exist. Skipping message ID {msg.id}."))
