from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Item


class ItemTests(APITestCase):
    def test_create_and_list_item(self):
        url = reverse("items")
        response = self.client.post(url, {"name": "Example", "description": "demo"}, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["name"], "Example")

