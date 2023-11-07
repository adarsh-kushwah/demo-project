from django.test import TestCase
from django.test import Client
from django.urls import reverse

from user.test_factory import UserFactory


class UserTest(TestCase):

    def setUp(self):
        self.owner = UserFactory()

    def test_login(self):
        self.owner_login = Client()
        response = self.owner_login.post(reverse("login"), {"username": self.owner.username, "password": self.owner.password})
        self.assertEqual(response.status_code, 200)
    
    def test_login_with_invalid_credentails(self):
        self.owner_login = Client()
        response = self.owner_login.post(reverse("login"), {"username": self.owner.username, "password": "invalid password"})
        valid_status = response.context[0]['form'].is_valid()
        self.assertEqual(valid_status, False)
        self.assertEqual(response.status_code, 200)

    def test_signup_existing_username(self):
        client = Client()
        duplicate_username_data = {
            'username' : self.owner.username,
            'user_type' : "owner",
            'gender' : 'male',
            'phone_number' : "1234567895",
            'password' : "Indore@123"
        }
        response = self.client.post(reverse("signup"),duplicate_username_data)
        status = dict(response.__dict__['context'][0]['errors'])['username'][0]
        self.assertEquals(status, "A user with that username already exists." )