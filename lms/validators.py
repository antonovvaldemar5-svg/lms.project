import re
from rest_framework.serializers import ValidationError


def validate_youtube_url(value):
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
    if not re.match(pattern, value):
        raise ValidationError('Разрешены только ссылки на YouTube')
