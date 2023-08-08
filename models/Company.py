from tortoise.fields import UUIDField, CharField, JSONField
from tortoise.models import Model


class Company(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=50)
    settings = JSONField()
