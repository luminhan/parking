import factory

from apps.authentication.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(lambda n: f"user{n}")
    email = factory.sequence(lambda n: f"user{n}@myproject.nl")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    account_status = "CONFIRMED"

    is_active = True
    is_staff = False
    is_superuser = False
