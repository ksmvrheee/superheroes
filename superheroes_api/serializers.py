from rest_framework import serializers
from .models import Hero


class HeroSerializer(serializers.ModelSerializer):
    """Serializer for the Hero model."""
    class Meta:
        model = Hero
        fields = '__all__'
