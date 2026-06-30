from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
        ('card', 'Банковская карта'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        'lms.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    paid_lesson = models.ForeignKey(
        'lms.Lesson',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default='card')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS, default='pending')

    class Meta:
        unique_together = ('user', 'paid_course', 'stripe_session_id')

    def __str__(self):
        return f'{self.user.email} - {self.amount}'


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions')
    course = models.ForeignKey(
        'lms.Course',
        on_delete=models.CASCADE,
        related_name='subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
