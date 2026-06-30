from rest_framework import serializers
from .models import Course, Lesson
from users.models import Payment
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'preview',
            'video_link',
            'course',
            'owner']
        read_only_fields = ['owner']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'preview',
            'lessons_count',
            'lessons',
            'owner',
            'is_subscribed']
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.subscriptions.filter(course=obj).exists()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
