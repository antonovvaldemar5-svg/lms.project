from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True)
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title