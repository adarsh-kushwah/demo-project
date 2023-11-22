import factory
from faker import Factory

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'user.UserProfile'

    username = faker.user_name()
    user_type = 'owner'
    gender = 'male'
    #phone_number = faker.phone_number()
    phone_number = faker.random_number(10)
    password = faker.password()

    # while len(phone_number) != 10 or not phone_number.isdigit():
    #     phone_number = faker.phone_number()

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", None)
        user = super(UserFactory, cls)._create(model_class, *args, **kwargs)
        user.set_password(password)
        user.save()
        return user