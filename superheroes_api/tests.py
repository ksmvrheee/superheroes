from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Hero


class HeroListCreateViewTests(APITestCase):
    """Tests for the views to create and list superheroes."""

    def setUp(self):
        self.url = '/hero/'

    @patch('superheroes_api.views.requests.get')
    def test_create_hero_success(self, mock_get):
        """Test successful hero creation via external API."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'response': 'success',
            'results': [{
                'name': 'Batman',
                'powerstats': {
                    'intelligence': '100',
                    'strength': '80',
                    'speed': '50',
                    'power': '60'
                }
            }]
        }

        response = self.client.post(self.url, {'name': 'Batman'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Batman')
        self.assertTrue(Hero.objects.filter(name='Batman').exists())

    def test_create_hero_no_name(self):
        """Test that missing 'name' field returns 400 error."""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_hero_already_exists(self):
        """Test that creating an existing hero returns 400 error."""
        Hero.objects.create(name='Batman')
        response = self.client.post(self.url, {'name': 'Batman'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    @patch('superheroes_api.views.requests.get')
    def test_create_hero_api_not_200(self, mock_get):
        """Test behavior when external API returns non-200 status."""
        mock_get.return_value.status_code = 500
        response = self.client.post(self.url, {'name': 'Batman'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertIn('error', response.data)

    @patch('superheroes_api.views.requests.get')
    def test_create_hero_response_not_success(self, mock_get):
        """Test behavior when external API response has 'error' status."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'response': 'error'}
        response = self.client.post(self.url, {'name': 'UnknownHero'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('superheroes_api.views.requests.get')
    def test_create_hero_no_exact_match(self, mock_get):
        """Test that hero is not created if names don't match exactly."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'response': 'success',
            'results': [{'name': 'NotBatman', 'powerstats': {}}]
        }
        response = self.client.post(self.url, {'name': 'Batman'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('superheroes_api.views.requests.get')
    def test_create_hero_invalid_stats(self, mock_get):
        """Test error handling when powerstats contain invalid values."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'response': 'success',
            'results': [{
                'not_a_name': 'Batman',
                'powerstats': {
                    'intelligence': 'null',
                    'strength': 'null',
                    'speed': 'null',
                    'power': 'null'
                }
            }]
        }
        response = self.client.post(self.url, {'name': 'Batman'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_list_heroes_success(self):
        """Test listing of existing heroes returns 200 with correct data."""
        Hero.objects.create(name='Batman', intelligence=100)
        Hero.objects.create(name='Superman', intelligence=95)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_heroes_no_results(self):
        """Test that 404 is returned when no heroes match the filter."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)
