from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
# my_app/management/commands/my_custom_startup_command.py

from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

# my_app/management/commands/my_custom_startup_command.py

from django.core.management.base import BaseCommand, CommandError
from sefas_admin.views import Day


class Command(BaseCommand):
    help = 'My custom startup command'

    def handle(self, *args, **kwargs):
        try:
        
            User = get_user_model()
            users = User.objects.all()
            for user in users:
                current =  datetime.today()
                for x in range (1, 365):
                    next_date = current + timedelta(days=x)
                    if next_date.weekday() > 4:
                           Day.objects.create(user=user, date=next_date.strftime('%Y-%m-%d'), hours=0.0)
        except:
            raise CommandError('Initalization failed.')