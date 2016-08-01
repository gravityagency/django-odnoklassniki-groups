from models import Group
import factory
import random

class GroupFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    members_count = random.randrange(0, 10000)

    class Meta:
        model = Group
