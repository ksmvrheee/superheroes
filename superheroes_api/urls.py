from django.urls import path

from superheroes_api.views import HeroListCreateView


urlpatterns = [
    path('hero/', HeroListCreateView.as_view(), name='hero-list-create'),
]
