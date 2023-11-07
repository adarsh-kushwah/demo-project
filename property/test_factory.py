import factory
from faker import Factory

from user.models import Location
from user.test_factory import UserFactory

faker = Factory.create()


class PropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'property.Property'

    owner = factory.SubFactory(UserFactory)
    name = faker.name()
    rent_amount = faker.random_number()

    while (rent_amount > 100000 or rent_amount < 1000 ):
        rent_amount = faker.random_number()
    