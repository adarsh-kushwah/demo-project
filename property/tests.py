from django.test import TestCase
from django.urls import reverse


class HomeTest(TestCase):

    def test_view(self):
        """
        testing home page
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class PropertyDetailTest(TestCase):

    def test_view(self):
        """
        testing property detail page
        """
        response = self.client.get(reverse('property_detail',kwargs={'property_id':1}))
        self.assertEqual(response.status_code, 200)