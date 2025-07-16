from django.db import models


class Hero(models.Model):
    """Represents a superhero that can have several characteristics."""
    name = models.CharField(unique=True, max_length=255)
    intelligence = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    speed = models.IntegerField(null=True)
    power = models.IntegerField(null=True)

    def __str__(self):
        return f'Hero "{self.name}"'

    class Meta:
        verbose_name_plural = 'heroes'
