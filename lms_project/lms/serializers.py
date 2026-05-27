from rest_framework import serializers
from .models import Course, Lesson
from users.models import Payment

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


