import requests
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from .filters import HeroFilter
from .models import Hero
from .serializers import HeroSerializer


API_URL = f'https://superheroapi.com/api/{settings.SUPERHEROAPI_TOKEN}/search/'

class HeroListCreateView(generics.ListCreateAPIView):
    """
    View for creating a superhero's object by grabbing the data from the superheroapi
    and for retrieving filtered data about one or several superheroes (uses HeroFilter).
    """
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HeroFilter

    def create(self, request, *args, **kwargs):
        """Creates a hero (POST method)."""
        name = request.data.get('name')
        if not name:
            return Response({'error': 'The "name" parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if Hero.objects.filter(name__iexact=name).exists():
            return Response({'error': 'The hero already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(API_URL + name)
        if response.status_code != 200:
            return Response({'error': 'An error occurred while trying '
                                      'to send a request to an external API.'}, status=status.HTTP_502_BAD_GATEWAY)

        data = response.json()
        if data['response'] != 'success':
            return Response({'error': 'No hero with such name was found.'}, status=status.HTTP_404_NOT_FOUND)

        for result in data['results']:
            try:
                if result['name'].lower() == name.lower():
                    intelligence = result['powerstats'].get('intelligence', '')
                    strength = result['powerstats'].get('strength', '')
                    speed = result['powerstats'].get('speed', '')
                    power = result['powerstats'].get('power', '')

                    hero = Hero.objects.create(
                        name=result['name'],
                        intelligence=int(intelligence) if intelligence.isdigit() else None,
                        strength=int(strength) if strength.isdigit() else None,
                        speed=int(speed) if speed.isdigit() else None,
                        power=int(power) if power.isdigit() else None,
                    )

                    serializer = self.get_serializer(hero)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            except (KeyError, ValueError):
                return Response({'error': 'Invalid response from the external API.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'No hero with such name was found.'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        """Retrieves some heroes (GET method)."""
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({'detail': 'No heroes match that filters.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
