from django.test import TestCase
from django.urls import reverse
from property.test_factory import UserFactory, PropertyFactory
from property.models import Property
from django.db.models.query import QuerySet
from django.test import Client

from user.models import UserProfile, UserAddress


class PropertyTest(TestCase):

    def setUp(self):
        self.owner = UserFactory()
        self.property = PropertyFactory(owner=self.owner)

    # def test_login(self):
    #     self.owner_login = Client()
    #     response = self.owner_login.post(reverse("login"), {"username": self.owner.username, "password": self.owner.password})
    #     self.assertEqual(response.status_code, 200)

    def test_with_several_property_by_one_owner(self):
        PropertyFactory.create_batch(5, owner=self.owner)
        self.properties = Property.objects.all()

        response = self.client.get(reverse('home'))
        
        self.assertEqual(type(self.properties), QuerySet)
        self.assertEqual(self.properties.count(),6)
        self.assertEqual(response.status_code, 200)

        for property in self.properties:
            self.assertContains(response, property.name)
        

    def test_single_property_detail(self):
        
        self.client.force_login(self.owner)
        response = self.client.get(reverse('property_detail', args=(self.property.id,) ) )
        self.assertEqual(response.status_code, 200)


    def test_home_page(self):
        """
        testing home page
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


# class PropertyDetailTest(TestCase):

#     def test_view(self):
#         """
#         testing property detail page
#         """
#         response = self.client.get(reverse('property_detail',kwargs={'property_id':1}))
#         self.assertEqual(response.status_code, 200)