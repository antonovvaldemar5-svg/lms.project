from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import User


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(
        last_login__lt=threshold, is_active=True)
    count = inactive_users.update(is_active=False)
    return f'Deactivated {count} users'
