from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from lms.models import Course, Lesson
from users.models import Subscription

User = get_user_model()


class LessonCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', password='123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Course', owner=self.user)
        self.lesson_data = {
            'title': 'Lesson',
            'description': 'Desc',
            'video_link': 'https://youtube.com/watch?v=abc',
            'course': self.course.id
        }

    def test_create_lesson(self):
        response = self.client.post('/api/lessons/', self.lesson_data)
        self.assertEqual(response.status_code, 201)

    def test_invalid_youtube_link(self):
        data = self.lesson_data.copy()
        data['video_link'] = 'https://vk.com/video'
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('YouTube', str(response.data))

    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            title='Lesson',
            description='Desc',
            video_link='https://youtube.com/watch?v=abc',
            course=self.course,
            owner=self.user
        )
        response = self.client.patch(
            f'/api/lessons/{lesson.id}/', {'title': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated')

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            title='Lesson',
            description='Desc',
            video_link='https://youtube.com/watch?v=abc',
            course=self.course,
            owner=self.user
        )
        response = self.client.delete(f'/api/lessons/{lesson.id}/')
        # только модератор может удалять
        self.assertEqual(response.status_code, 403)


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', password='123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Course', owner=self.user)

    def test_add_subscription(self):
        response = self.client.post(
            '/api/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course).exists())

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(
            '/api/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course).exists())
