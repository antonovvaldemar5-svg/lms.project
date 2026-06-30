from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course
from users.models import Subscription


@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)
        emails = [sub.user.email for sub in subscriptions if sub.user.email]

        if emails:
            send_mail(
                subject=f'Курс "{course.title}" обновлён',
                message='В курсе появились новые материалы. Зайдите и посмотрите.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )
    except Course.DoesNotExist:
        pass
