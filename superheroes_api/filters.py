import django_filters
from .models import Hero


class HeroFilter(django_filters.FilterSet):
    """Filters for searching for heroes by name and numerical characteristics."""
    name = django_filters.CharFilter(lookup_expr='iexact')  # case-independent

    intelligence = django_filters.NumberFilter()
    intelligence__gt = django_filters.NumberFilter(field_name='intelligence', lookup_expr='gt')
    intelligence__lt = django_filters.NumberFilter(field_name='intelligence', lookup_expr='lt')
    intelligence__gte = django_filters.NumberFilter(field_name='intelligence', lookup_expr='gte')
    intelligence__lte = django_filters.NumberFilter(field_name='intelligence', lookup_expr='lte')

    strength = django_filters.NumberFilter()
    strength__gt = django_filters.NumberFilter(field_name='strength', lookup_expr='gt')
    strength__lt = django_filters.NumberFilter(field_name='strength', lookup_expr='lt')
    strength__gte = django_filters.NumberFilter(field_name='strength', lookup_expr='gte')
    strength__lte = django_filters.NumberFilter(field_name='strength', lookup_expr='lte')

    speed = django_filters.NumberFilter()
    speed__gt = django_filters.NumberFilter(field_name='speed', lookup_expr='gt')
    speed__lt = django_filters.NumberFilter(field_name='speed', lookup_expr='lt')
    speed__gte = django_filters.NumberFilter(field_name='speed', lookup_expr='gte')
    speed__lte = django_filters.NumberFilter(field_name='speed', lookup_expr='lte')

    power = django_filters.NumberFilter()
    power__gt = django_filters.NumberFilter(field_name='power', lookup_expr='gt')
    power__lt = django_filters.NumberFilter(field_name='power', lookup_expr='lt')
    power__gte = django_filters.NumberFilter(field_name='power', lookup_expr='gte')
    power__lte = django_filters.NumberFilter(field_name='power', lookup_expr='lte')

    class Meta:
        model = Hero
        fields = [
            'name',
            'intelligence', 'intelligence__gt', 'intelligence__lt', 'intelligence__gte', 'intelligence__lte',
            'strength', 'strength__gt', 'strength__lt', 'strength__gte', 'strength__lte',
            'speed', 'speed__gt', 'speed__lt', 'speed__gte', 'speed__lte',
            'power', 'power__gt', 'power__lt', 'power__gte', 'power__lte',
        ]
